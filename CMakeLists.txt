cmake_minimum_required(VERSION 3.24)
project(csapp C)

set(CMAKE_C_STANDARD 99)

include_directories(src)

add_executable(csapp
        src/common/convert.c
        src/common/print.c
        src/hardware/cpu/isa.c
        src/hardware/cpu/mmu.c
        src/hardware/memory/dram.c
        src/headers/common.h
        src/headers/cpu.h
        src/headers/memory.h
        src/tests/test_hardware.c)
