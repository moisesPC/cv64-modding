INCLUDE linker/extern.ld

SECTIONS
{
    /* Discard this section so that it doesnt get between .rodata and .bss */
    /* Ensuring that the .text, .data, .rodata and .bss are always the first four sections in the ELF */
    /DISCARD/ : {
        *(.MIPS.abiflags)
    }

    . = VRAM_ADDRESS;

    .text : 
    {
        __text_start = .;
        *(.text)
        *(.text.*)
        . = ALIGN(16);
        __text_end = .;
    }

    .data ALIGN(16) : 
    {
        __data_start = .;
        *(.data)
        *(.data.*)
        . = ALIGN(16);
        __data_end = .;
    }

    .rodata ALIGN(16) : 
    {
        __rodata_start = .;
        *(.rodata)
        *(.rodata.*)
        . = ALIGN(16);
        __rodata_end = .;
    }
    
    .bss ALIGN(16): 
    {
        __bss_start = .;
        *(.bss)
        *(.bss.*)
        . = ALIGN(16);
        __bss_end = .;
    }
}
