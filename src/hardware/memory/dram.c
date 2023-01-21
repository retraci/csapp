// Dynamic Random Access Memory
#include <string.h>
#include <assert.h>
#include "headers/cpu.h"
#include "headers/memory.h"
#include "headers/common.h"
#include "headers/address.h"

uint8_t sram_cache_read(uint64_t paddr);
void sram_cache_write(uint64_t paddr, uint8_t data);

/*
 * Be careful with the x86-64 little endian integer encoding
 * e.g. write 0x00007fd357a02ae0 to cache, the memory lapping should be:
 *   e0 2a a0 57 d3 7f 00 00
 *
*/

// memory accessing used in instructions
uint64_t cpu_read64bits_dram(uint64_t paddr) {
    if (DEBUG_ENABLE_SRAM_CACHE) {
        // try to load uint64_t from SRAM cache
        // little-endian
        uint64_t val = 0x0;
        for (int i = 0; i < 8; i++) {
            val += sram_cache_read(paddr + i) << (i * 8);
        }
        return val;
    } else {
        // read from DRAM directly
        // little-endian
        uint64_t val = 0x0;
        for (int i = 0; i < 8; i++) {
            val += ((uint64_t) pm[paddr + i]) << (i * 8);
        }
        return val;
    }
}

void cpu_write64bits_dram(uint64_t paddr, uint64_t data) {
    if (DEBUG_ENABLE_SRAM_CACHE) {
        // try to write uint64_t to SRAM cache
        // little-endian
        for (int i = 0; i < 8; i++) {
            sram_cache_write(paddr + i, (data >> (i * 8)) & 0xff);
        }
    } else {
        // little-endian
        // write to DRAM directly
        for (int i = 0; i < 8; i++) {
            pm[paddr + i] = (data >> (i * 8)) & 0xff;
        }
    }
}

void cpu_readinst_dram(uint64_t paddr, char *buf) {
    for (int i = 0; i < MAX_INSTRUCTION_CHAR; i++) {
        buf[i] = (char) pm[paddr + i];
    }
}

void cpu_writeinst_dram(uint64_t paddr, const char *str) {
    int len = strlen(str);
    assert(len < MAX_INSTRUCTION_CHAR);

    for (int i = 0; i < MAX_INSTRUCTION_CHAR; i++) {
        pm[paddr + i] = i < len ? (uint8_t) str[i] : 0;
    }
}


/*
 * interface of I/O Bus: read and write between the SRAM cache and DRAM memory
 */

void bus_read_cacheline(uint64_t paddr, uint8_t *block) {
    uint64_t dram_base = ((paddr >> SRAM_CACHE_OFFSET_LENGTH) << SRAM_CACHE_OFFSET_LENGTH);

    for (int i = 0; i < (1 << SRAM_CACHE_OFFSET_LENGTH); i++) {
        block[i] = pm[dram_base + i];
    }
}

void bus_write_cacheline(uint64_t paddr, uint8_t *block) {
    uint64_t dram_base = ((paddr >> SRAM_CACHE_OFFSET_LENGTH) << SRAM_CACHE_OFFSET_LENGTH);

    for (int i = 0; i < (1 << SRAM_CACHE_OFFSET_LENGTH); i++) {
        pm[dram_base + i] = block[i];
    }
}
