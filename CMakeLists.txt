cmake_minimum_required(VERSION 3.24)
project(csapp C)

set(CMAKE_C_STANDARD 99)

include_directories(src)

add_executable(csapp
        src/algorithm/array.c
        src/algorithm/bst.c
        src/algorithm/hashtable.c
        src/algorithm/linkedlist.c
        src/algorithm/redblack.c
        src/algorithm/trie.c

        src/common/cleanup.c
        src/common/convert.c
        src/common/tagmalloc.c

        src/hardware/cpu/isa.c
        src/hardware/cpu/mmu.c
        src/hardware/cpu/sram.c
        src/hardware/memory/dram.c
        src/hardware/memory/swap.c

        src/headers/address.h
        src/headers/algorithm.h
        src/headers/common.h
        src/headers/cpu.h
        src/headers/instruction.h
        src/headers/linker.h
        src/headers/memory.h

        src/mains/false_sharing.c
        src/mains/mesi.c

        src/linker/parseElf.c
        src/linker/staticlink.c

        )
