cmake_minimum_required(VERSION 3.24)
project(csapp C)

set(CMAKE_C_STANDARD 99)

include_directories(src)

add_executable(csapp
        src/algorithm/array.c
        src/algorithm/bst.c
        src/algorithm/hashtable.c
        src/algorithm/linkedlist.c
        src/algorithm/rbt.c
        src/algorithm/trie.c

        src/common/cleanup.c
        src/common/convert.c

        src/hardware/cpu/inst.c
        src/hardware/cpu/isa.c
        src/hardware/cpu/mmu.c
        src/hardware/cpu/sram.c
        src/hardware/memory/dram.c
        src/hardware/memory/swap.c

        src/headers/address.h
        src/headers/algorithm.h
        src/headers/allocator.h
        src/headers/common.h
        src/headers/cpu.h
        src/headers/instruction.h
        src/headers/linker.h
        src/headers/memory.h

        src/linker/parseElf.c
        src/linker/staticlink.c

        src/mains/false_sharing.c
        src/mains/mesi.c

        src/malloc/block.c
        src/malloc/explicit_list.c
        src/malloc/implicit_list.c
        src/malloc/mem_alloc.c
        src/malloc/redblack_tree.c
        src/malloc/segregated_list.c
        src/malloc/small_list.c

        src/tests/test_bst.c
        src/tests/test_convert.c
        src/tests/test_inst.c
        src/tests/test_malloc.c
        src/tests/test_rbt.c
        src/tests/test_run_isa.c
        src/tests/test_trie.c

        )
