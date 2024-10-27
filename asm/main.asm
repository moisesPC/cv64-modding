.include "asm/extern.asm"
.include "asm/sections.asm"

.n64
.open INPUTROM, OUTPUTROM, 0x0

/******************** Custom segment loader ********************/

.headersize SEC_MAIN_HEADERSIZE

.org 0x80079A58
    // Overwrite useless branch in one of the bootup functions
    jal load_custom_segment
    nop

.headersize SEC_COMMON_HEADERSIZE

.org 0x8018BF98
// Ensure we can only write up to 0x460 bytes from 0x8018BF98,
// since there's data used by the game's code afterwards
.area 0x460, 0
load_custom_segment:
    addiu sp, sp, -0x18
    sw    ra, 0x14 (sp)
    la    t0, SEC_STATIC_SIZE
    la    a0, SEC_STATIC_ROM
    la    a1, SEC_STATIC_RAM
    jal   dma_rom_copy
    addu  a2, a1, t0
    nop
    jal   customSegment_init
    nop
    lw    ra, 0x14 (sp)
    jr    ra
    addiu sp, sp, 0x18

.endarea

/******************** Hooks ********************/

.headersize SEC_MAIN_HEADERSIZE

// Called once every frame after the game has been initialized
// Overwrites call to `controller_readData`
.org 0x80015390
    jal customSegment_loop

/******************** Custom segment ********************/

.headersize SEC_STATIC_HEADERSIZE
.org SEC_STATIC_RAM
/* NOTE: This will pad this area with 0. Make sure you don't have anything placed on this area before executing ARMIPS */
.area SEC_STATIC_SIZE, 0

.importobj "build/src/static/static_segment.bin.o"
.align 4

.if . > SEC_STATIC_RAM + SEC_STATIC_SIZE
    .error "Custom segment overflow"
.endif

.endarea

.close
