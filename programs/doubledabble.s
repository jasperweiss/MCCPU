define a 99

_start:
    ldi r1 a
    ldi r3 0x0
    ldi r4 screen
    ldi r7 0x8
clear:
    str r4 r3
    inc r4
    str r4 r3
    inc r4
    str r4 r3
    inc r4
    str r4 r3
    inc r4
    ldi r4 screen
loop:
    ldi r6 #0b0100
    ldi r2 #0b1111
    and r2 r2 r3
    cmp r6 r2
    bif carry .skip0
    ldi r6 #0b011
    add r3 r3 r6

.skip0:
    ldi r6 #0b01000000
    ldi r2 #0b11110000
    and r2 r2 r3
    cmp r6 r2
    bif carry .skip1
    ldi r6 #0b00110000
    add r3 r3 r6

.skip1:
    lsh r3 r3
    lsh r1 r1
    adc r3 r3 r0
    dec r7 r7
    cmp r7 r0
    str r4 r3
    bif !zero loop

.done
    hlt