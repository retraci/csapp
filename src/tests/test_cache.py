#!/usr/bin/python3
# usage: 
#   ./cmd.py argv[1] argv[2], ...
#   /usr/bin/python3 ./cmd.py argv[1] argv[2], ...
import sys
import os
import subprocess
from ctypes import *
from functools import reduce

debug = False


def scan_ints(s):
    results = []
    i = 0
    # state = 0 - not in a number
    # state = 1 - in a number
    state = 0
    while i < len(s):
        # I cannot bear the casting system in python
        # especially for the bytes and chars and ints
        c = ord(s[i])

        if state == 0 and ord('0') <= c and c <= ord('9'):
            # switch from state 0 to state 1
            state = 1
            results += [0]
        elif state == 1 and not (ord('0') <= c and c <= ord('9')):
            state = 0

        if state == 1:
            results[-1] = results[-1] * 10 + int(c - ord('0'))
        i += 1

    assert (len(results) == 5)
    return results


def run_csim_ref(s, E, b, trace_file, csim_ref_file):
    # ./csim -s 0 -E 1 -b 0 -t traces/wide.trace

    proc = subprocess.run([
        csim_ref_file,
        "-v",
        "-s", str(s),
        "-E", str(E),
        "-b", str(b),
        "-t", trace_file
    ], cwd=os.path.dirname(csim_ref_file), stdout=subprocess.PIPE)

    out = proc.stdout.decode("ASCII")
    # L 37f, 1 miss
    # L 37b, 1 hit

    data = out.split("\n")
    stat_line = ""
    ref_trace = []
    for line in data:
        if line.endswith("hit"):
            ref_trace += ["hit"]
        elif line.endswith("miss"):
            ref_trace += ["miss"]
        elif line.endswith("miss eviction"):
            ref_trace += ["miss eviction"]
        elif line.startswith("hits:"):
            stat_line = line

    return scan_ints(stat_line), ref_trace


def read_trace(trace_file):
    try:
        with open(trace_file, "r", encoding='ascii') as fr:
            content = fr.readlines()
            results = []
            for line in content:
                # parse trace line
                #   L 7ff000384,4
                #   S 7ff000388,4
                split_space = (line.strip(" ")).split(" ")
                assert (len(split_space) == 2)

                op = split_space[0]
                assert (op == "L" or op == "S")

                split_comma = (split_space[1]).split(",")
                assert (len(split_comma) == 2)

                paddr = int("0x" + split_comma[0], 16)

                bsize = int(split_comma[1])
                assert (bsize == 1 or bsize == 2 or bsize == 4 or bsize == 8)

                results += [[op, paddr, bsize]]
            return results
    except UnicodeDecodeError:
        return None


def print_stat(lib):
    print(
        (c_int.in_dll(lib, "cache_hit_count")).value,
        (c_int.in_dll(lib, "cache_miss_count")).value,
        (c_int.in_dll(lib, "cache_evict_count")).value,
        (c_int.in_dll(lib, "dirty_bytes_in_cache_count")).value,
        (c_int.in_dll(lib, "dirty_bytes_evicted_count")).value,
    )


def run_csim(s, E, b, trace_file):
    # compile
    subprocess.run(
        [
            "/usr/bin/gcc",
            "-Wall", "-g", "-O0", "-Werror", "-std=gnu99", "-Wno-unused-function",
            "-I", "./src",
            "-DCACHE_SIMULATION_VERIFICATION",  # define not to call the dram functions
            "-DSRAM_CACHE_INDEX_LENGTH=%d" % s,
            "-DSRAM_CACHE_OFFSET_LENGTH=%d" % b,
            "-DNUM_CACHE_LINE_PER_SET=%d" % E,
            "-DSRAM_CACHE_TAG_LENGTH=%d" % (64 - s - b),
            "-shared", "-fPIC",
            "./src/hardware/cpu/sram.c",
            "-ldl", "-o", "./bin/csim.so"
        ])

    # read trace file
    trace = read_trace(trace_file)
    # load shared library
    lib = cdll.LoadLibrary("./bin/csim.so")

    test_trace = []
    i = 0
    pass_trace = True
    for [op, paddr, bsize] in trace:
        if debug:
            print(op, "0x%lx" % paddr, bsize)
            print_paddr(paddr, s, b)

        if op == "L":
            lib.sram_cache_read(c_ulonglong(paddr))
        elif op == "S":
            lib.sram_cache_write(c_ulonglong(paddr), c_byte(1))

        if debug:
            lib.print_cache()
            lib.fflush(None)

        cache_behavior = (c_char_p.in_dll(lib, "trace_ptr")).value.decode("ascii")
        test_trace.append(cache_behavior)

        if debug:
            print_stat(lib)

        i += 1

    return [
        (c_int.in_dll(lib, "cache_hit_count")).value,
        (c_int.in_dll(lib, "cache_miss_count")).value,
        (c_int.in_dll(lib, "cache_evict_count")).value,
        (c_int.in_dll(lib, "dirty_bytes_in_cache_count")).value,
        (c_int.in_dll(lib, "dirty_bytes_evicted_count")).value,
    ], test_trace


def check_trace(ref_trace, test_trace):
    if len(ref_trace) != len(test_trace):
        return False

    i = 0
    pass_trace = True
    for i in range(len(test_trace)):
        if debug:
            print("test:", test_trace[i], "ref:", ref_trace[i])
        if test_trace[i] != ref_trace[i]:
            print("[%d] conflict!" % i)
            pass_trace = False
            break
        i += 1
    return pass_trace


def cache_test(s, E, b, trace_file, csim_ref_file):
    ref_stat, ref_trace = run_csim_ref(s, E, b, trace_file, csim_ref_file)
    test_stat, test_trace = run_csim(s, E, b, trace_file)

    pass_stat = reduce((lambda x, y: x and y), [test_stat[i] == ref_stat[i] for i in range(len(ref_stat))])
    pass_trace = check_trace(ref_trace, test_trace)

    if pass_stat and pass_trace:
        return True
    else:
        print(pass_stat, pass_trace)
        print(ref_stat)
        print(test_stat)
        return False


def print_paddr(paddr, s, b):
    p = [2 ** i for i in range(64)]
    string_hex = lambda b: "0x%lx" % reduce((lambda x, y: x + y), [b[i] * p[i] for i in range(len(b))])
    string_binary = lambda b: "".join([str(b[i]) for i in range(len(b) - 1, -1, -1)])

    bits = []
    for i in range(64):
        bits += [(paddr & 0x1)]
        paddr = (paddr >> 1)
    boffset = bits[0: b]
    bindex = bits[b: b + s]
    btag = bits[b + s: 64]

    print_table(
        [
            ["tag", "index", "offset"],
            [string_binary(btag), string_binary(bindex), string_binary(boffset)],
            [string_hex(btag), string_hex(bindex), string_hex(boffset)]
        ]
    )


def print_table(data):
    nr = len(data)
    nc = len(data[0])
    width = [4 * (int(max([len(data[j][i]) + 2 for j in range(nr)]) / 4) + 1) for i in range(nc)]

    bar = "+"
    for w in width:
        for i in range(w):
            bar += "-"
        bar += "+"

    def format_line(line):
        temp = "|"
        for j in range(nc):
            temp += " "
            temp += line[j]
            for k in range(width[j] - len(line[j]) - 1):
                temp += " "
            temp += "|"
        return temp

    # print header
    print(bar)
    print(format_line(data[0]))
    print(bar)
    i = 1
    while i < len(data):
        print(format_line(data[i]))
        i += 1
    print(bar)


# print arguments

if __name__ == '__main__':
    assert (len(sys.argv) in {6, 7})

    csim_ref_file = sys.argv[1]
    trace_file = sys.argv[2]
    s = int(sys.argv[3])
    E = int(sys.argv[4])
    b = int(sys.argv[5])

    if len(sys.argv) == 7:
        debug = True

    assert (os.path.isfile(csim_ref_file))
    assert (os.path.isfile(trace_file))

    if cache_test(s, E, b, trace_file, csim_ref_file):
        print("Pass")
    else:
        print("Fail")
