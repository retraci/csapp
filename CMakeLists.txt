cmake_minimum_required(VERSION 3.24)
project(csapp C)

set(CMAKE_C_STANDARD 99)

include_directories(src)

add_executable(csapp
        src/headers/instruction.h
        src/headers/common.h
        src/headers/cpu.h
        src/headers/memory.h
        src/headers/algorithm.h
        src/common/convert.c
        src/common/print.c
        src/common/cleanup.c
        src/common/tagmalloc.c
        src/hardware/cpu/isa.c
        src/hardware/cpu/mmu.c
        src/hardware/memory/dram.c
        src/algorithm/array.c
        src/algorithm/hashtable.c
        src/algorithm/linkedlist.c
        src/algorithm/trie.c
        src/tests/test_machine.c
        src/tests/test_elf.c
        src/linker/parseElf.c
        src/linker/linker.c
        src/linker/staticlink.c)
