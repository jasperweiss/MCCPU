    ldi r7 0x23     ; biggest memory address
    ldi r1 0xFF
    ldi r2 0x00
    ldi r6 screen   ; start address of screen (little endian)
clear:
    str r7 r2
    dec r7 r7
    cmp r7 r6
    bif carry clear
    str r6 r7
loop:
    str r7 r1
    dec r7 r7
    str r6 r7
    cmp r7 r0
    bif !zero loop
    cmp r1 r2
    bif zero done
    cpy r1 r2
    ldi r7 0x1F
    jmp loop
done:
    hlt
