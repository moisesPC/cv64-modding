.include "../asm/extern.asm"
.include "../asm/sections.asm"

/******************** Custom segment loader ********************/

.headersize SEC_MAIN_HEADERSIZE

.org 0x80079A58
    // Overwrite useless branch in one of the bootup functions
    jal load_custom_segment
    nop

.headersize SEC_COMMON_HEADERSIZE

.org 0x8018BF98
// Unsure we can only write up to 0x460 bytes from 0x8018BF98,
// since there's data used by the game's code afterwards
.area 0x460, 0
load_custom_segment:
    addiu sp, sp, -0x18
    sw    ra, 0x14 (sp)
    la    t0, SEC_CUSTOM_SIZE
    la    a0, SEC_CUSTOM_ROM
	la    a1, SEC_CUSTOM_RAM
	jal   dma_rom_copy
    addu  a2, a1, t0
	nop
    jal   hook_customSegmentInit
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
    jal hook_customSegmentLoop

/******************** Custom segment ********************/

.headersize SEC_CUSTOM_HEADERSIZE
.org SEC_CUSTOM_RAM
.area SEC_CUSTOM_SIZE, 0

// Import the custom segment with all code and data compiled from src/sec_custom
// into the ROM

.importlib "../build/build/sec_custom.a"
.align 4

.endarea // SEC_CUSTOM_SIZE
