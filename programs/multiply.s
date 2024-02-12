
define a 234
define b 48

.start
    ldi r1 a
    ldi r2 b
    ldi r3 0x0       // r2 overflow
    ldi r4 0x0       // answer bytes 8:0
    ldi r5 0x0       // answer bytes 16:8
    ldi r6 0x1       // const 1
    ldi r7 screen

.loop
    cmp r1 r0
    bif zero .done
    and r0 r1 r6
    bif zero .skip
    add r4 r4 r2
    adc r5 r5 r3
    bif carry .fault

.skip
    rsh r1 r1
    lsh r3 r3
    bif carry .fault
    lsh r2 r2
    adc r3 r3 r0
    bif carry .fault
    jmp .loop

.done
    str r7 r4
    inc r7 r7
    str r7 r5
    hlt

.fault
    ldi r5 0xf
    str r7 r5
    hlt


