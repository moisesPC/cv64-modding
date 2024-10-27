/********** This file contains definitions for the addresses                    **********/
/********** of different sections where code resides, not only the ones found   **********/
/********** in the ROM by default, but also out custom ones where we'll put our **********/
/********** custom code                                                         **********/

.ifndef _SECTIONS_ASM_
.definelabel _SECTIONS_ASM_, 1

.definelabel ROM_PADDING_START,  0x00BB2D88
.definelabel ROM_PADDING_END,    0x00C00000
.definelabel RAM_EXPANSION_PAK_START,    0x80400000
.definelabel RAM_EXPANSION_PAK_END,      0x80800000

/********** Existing sections **********/

.definelabel SEC_MAIN_ROM, 0x00001060
.definelabel SEC_MAIN_RAM, 0x80000460
.definelabel SEC_MAIN_HEADERSIZE, (SEC_MAIN_RAM - SEC_MAIN_ROM)
.definelabel SEC_MAIN_SIZE, 0x000E1E98

.definelabel SEC_COMMON_ROM, 0x000A8420
.definelabel SEC_COMMON_RAM, 0x80125230
.definelabel SEC_COMMON_HEADERSIZE, (SEC_COMMON_RAM - SEC_COMMON_ROM)
.definelabel SEC_COMMON_SIZE, 0x000698E0

.definelabel SEC_10FC40_ROM, 0x0010FC40
.definelabel SEC_10FC40_RAM, 0x80389F10
.definelabel SEC_10FC40_HEADERSIZE, (SEC_10FC40_RAM - SEC_10FC40_ROM)
.definelabel SEC_10FC40_SIZE, 0x000065D0

.definelabel SEC_REINHARDT_ROM, 0x00697040
.definelabel SEC_REINHARDT_RAM, 0x803D13E0
.definelabel SEC_REINHARDT_HEADERSIZE, (SEC_REINHARDT_RAM - SEC_REINHARDT_ROM)
.definelabel SEC_REINHARDT_SIZE, 0x0000D290

.definelabel SEC_CARRIE_ROM, 0x006A42D0
.definelabel SEC_CARRIE_RAM, 0x803D13E0
.definelabel SEC_CARRIE_HEADERSIZE, (SEC_CARRIE_RAM - SEC_CARRIE_ROM)
.definelabel SEC_CARRIE_SIZE, 0x0000D020

/********** Custom section example **********/

// Example custom section, where code and data will be stored at the following places:
// ROM: Start of ROM's padding (0x00BB2D88)
// RAM: Start of RAM's unused space before Expansion Pak memory (0x803FB270)

.definelabel SEC_STATIC_ROM,  ROM_PADDING_START
.definelabel SEC_STATIC_RAM,  0x803FB270
.definelabel SEC_STATIC_HEADERSIZE, (SEC_STATIC_RAM - SEC_STATIC_ROM)
// Size of the available RAM space starting from 0x803FB270 until Expansion Pak memory (0x80400000)
.definelabel SEC_STATIC_SIZE, (RAM_EXPANSION_PAK_START - SEC_STATIC_RAM)

.endif // _SECTIONS_ASM_
