// Dynamic Random Access Memory
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "headers/cpu.h"
#include "headers/memory.h"
#include "headers/common.h"
#include "headers/address.h"

// each swap file is swap page
// each line of this swap page is one uint64
#define SWAP_PAGE_FILE_LINES (512)

// disk address counter
static uint64_t internal_swap_daddr = 0;

void swap_in(uint64_t daddr, uint64_t ppn) {
    FILE *fr = NULL;
    char filename[128];
    sprintf(filename, "../files/swap/page-%ld.txt", daddr);
    fr = fopen(filename, "r");
    assert(fr != NULL);

    uint64_t base = ppn << PHYSICAL_PAGE_OFFSET_LENGTH;
    char buf[64] = {'\0'};
    for (int i = 0; i < SWAP_PAGE_FILE_LINES; i++) {
        char *str = fgets(buf, 64, fr);
        *((uint64_t *) (&pm[base + i * 8])) = string2uint(str);
    }
    fclose(fr);
}

void swap_out(uint64_t daddr, uint64_t ppn) {
    FILE *fw = NULL;
    char filename[128];
    sprintf(filename, "../files/swap/page-%ld.txt", daddr);
    fw = fopen(filename, "w");
    assert(fw != NULL);

    uint64_t base = ppn << PHYSICAL_PAGE_OFFSET_LENGTH;
    for (int i = 0; i < SWAP_PAGE_FILE_LINES; i++) {
        fprintf(fw, "0x%16lx\n", *((uint64_t *) (&pm[base + i * 8])));
    }
    fclose(fw);
}
