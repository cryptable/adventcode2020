ENTRY(_start)
 
SECTIONS
{
    . = 0x80000;
    .text :
    {
        KEEP(*(.text.start))
        *(.text .text.*)
    }
    . = ALIGN(32);
 
    .rodata :
    {
        *(.rodata .rodata.*)
    }
    . = ALIGN(32);
 
    .data :
    {
        *(.data .data.*)
    }
    . = ALIGN(32);
 
    __bss_start = .;
    .bss :
    {
        bss = .;
        *(.bss .bss.*)
    }
    . = ALIGN(32);
    __bss_end = .;
    __bss_size = __bss_end - __bss_start;
}