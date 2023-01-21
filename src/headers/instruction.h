// include guards to prevent double declaration of any identifiers
// such as types, enums and static variables
#ifndef INSTRUCTION_GUARD
#define INSTRUCTION_GUARD

#include <stdint.h>

/*======================================*/
/*      instruction set architecture    */
/*======================================*/

typedef enum OPERAND_TYPE {
    OD_EMPTY,                  // 0
    OD_IMM,                    // 1
    OD_REG,                    // 2
    OD_MEM_IMM,                // 3
    OD_MEM_REG1,               // 4
    OD_MEM_IMM_REG1,           // 5
    OD_MEM_REG1_REG2,          // 6
    OD_MEM_IMM_REG1_REG2,      // 7
    OD_MEM_REG2_SCAL,          // 8
    OD_MEM_IMM_REG2_SCAL,      // 9
    OD_MEM_REG1_REG2_SCAL,     // 10
    OD_MEM_IMM_REG1_REG2_SCAL  // 11
} od_type_t;

typedef struct OPERAND_STRUCT {
    od_type_t type;   // OD_IMM, OD_REG, OD_MEM
    uint64_t imm;    // immediate number
    uint64_t scal;   // scale number to register 2
    uint64_t reg1;   // main register
    uint64_t reg2;   // register 2
} od_t;

// handler table storing the handlers to different instruction types
typedef void (*op_t)(od_t *, od_t *);

// local variables are allocated in stack in run-time
// we don't consider local STATIC variables
// ref: Computer Systems: A Programmer's Perspective 3rd
// Chapter 7 Linking: 7.5 Symbols and Symbol Tables
typedef struct INST_STRUCT {
    op_t op;         // enum of operators. e.g. mov, call, etc.
    od_t src;        // operand src of instruction
    od_t dst;        // operand dst of instruction
} inst_t;

#define MAX_NUM_INSTRUCTION_CYCLE 100

#endif
