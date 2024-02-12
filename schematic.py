import mcschematic

def make_schematic(machinecode_filename, path, name, version):
    rom = open(machinecode_filename, 'rb').read()

    lines = [bin(rom[i])[2:].rjust(8, '0')+bin(rom[i+1])[2:].rjust(8, '0') for i in range(0,len(rom),2)]
    # for i in range(0,len(rom),2):
    #     print(bin(rom[i])[2:].rjust(8, '0'),bin(rom[i])[2:].rjust(8, '0'))

    # swap byte 1 <-> byte 2
    for i, line in enumerate(lines):
        byte_1 = line[0:8]
        byte_2 = line[8:16]
        lines[i] = byte_2[::-1] + byte_1

    # fill to 64 lines
    noop = '0000000000000000'
    while (len(lines) < 64):
        lines.append(noop)

    pos = [9, -15, 2]

    schem = mcschematic.MCSchematic()

    # generate bottom bit locations for the right side
    right_side = []

    for _ in range(2):
        # row 1 and 3
        for i in range(8):
            if i % 2 == 1:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] += 2
            pos[1] = -15

        pos[2] -= 3

        for i in range(8):
            if i % 2 == 0:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] -= 2
            pos[1] = -15

        pos[2] += 2
        pos[0] += 8

        # row 2 and 4
        for i in range(8):
            if i % 2 == 1:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] += 2
            pos[1] = -15

        pos[2] -= 1

        for i in range(8):
            if i % 2 == 0:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] -= 2
            pos[1] = -15

        pos[2] += 2
        pos[0] += 8


    # generated bottom bit locations for left side (flip z values of right side)
    left_side = []
    for bottom_bit in right_side:
        left_side.append([bottom_bit[0], bottom_bit[1], -bottom_bit[2]])

    # place barrels
    on_block = 'minecraft:barrel{Items:[{Slot:0,id:redstone,Count:1}]}'
    for pleft, pright, binary in zip(left_side, right_side, lines):
        for bit in binary[0:8]:
            if bit == '1':
                schem.setBlock(tuple(pright), on_block)
            pright[1] += 2

        for bit in binary[8:16][::-1]:
            if bit == '1':
                schem.setBlock(tuple(pleft), on_block)
            pleft[1] += 2

    schem.save(path, name, version)
    print("\nSchematic saved to", f"{name}.schem")