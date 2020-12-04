// AArch64 mode
 
// This file will be kept as first (see linker script).
.section ".text.start"
 
// Make _start global.
.globl _start
 
_start: 
    mrs     x1, mpidr_el1
    and     x1, x1, #3
    cbz     x1, 2f
1:   
    wfe
    b       1b

2:
    ldr     x5, =_start
    mov     sp, x5
 
    // clear bss
    ldr     x5, =__bss_start
    ldr     w6, =__bss_size
3:  cbz     w6, 4f
    str     xzr, [x5], #8
    sub     w6, w6, #1
    cbnz    w6, 3b
 
    // jump to C code, should not return
4:  bl      rmain
    // for failsafe, halt this core too
    b       1b
