def assemble(assembly_filename, output_filename):
    assembly_file = open(assembly_filename, 'r')
    machine_code_file = open(output_filename, 'wb')
    lines = (line for line in assembly_file)

    def remove_comment(comment_symbol, line):
        head, _, _ = line.partition(comment_symbol)
        return head

    # remove comments and blanklines
    lines = [remove_comment("//", line) for line in lines]
    lines = [remove_comment(";", line) for line in lines]
    lines = [line for line in lines if not line.isspace()]

    # create symbols
    symbols = {
        'screen': 0x20,
    }

    registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    opcodes = ['nop', 'hlt', 'add', 'sub', 'xor', 'orr', 'and', 'inc', 'dec', 'rsh', 'not', 'ldi', 'lod', 'str', 'bif']
    for index, symbol in enumerate(opcodes):
        symbols[symbol] = index

    conditions = ['carry', '!carry', 'zero', '!zero', 'reserved1', 'reserved2', 'reserved3', 'always']
    for index, symbol in enumerate(conditions):
        symbols[symbol] = index

    carry = ['without_carry', 'with_carry']
    for index, symbol in enumerate(carry):
        symbols[symbol] = index

    def is_definition(word):
        return word == 'define'

    def is_label(line):
        return not line[0] in [' ', '\t']

    # add definitions and labels to symbol table
    # expects all definitions to be above assembly
    index = 0
    code = []
    for line in lines:
        words = line.split()
        if is_definition(words[0]):
            symbols[words[1]] = int(words[2])
        elif is_label(line):
            symbols[words[0].replace(":","")] = index
            code.append((index,line))
        else:
            code.append((index,line))
            index += 1

    # generate machine code
    def resolve(word):
        if word.startswith('0x'):
            return int(word, 16)
        elif word.startswith('#0b'):
            return int(word[1:], 2)
        elif word[0] == '#':
            return int(word[1:])
        return symbols.get(word)

    print(f'Address\t opp  args args')

    machine_code = bytearray()
    for index, line in code:
        if is_label(line):
            print(f'\n{line.strip()}')
            continue
        words = line.split()
        words = [word.lower() for word in words]

        # special ops
        if words[0] == 'lsh':
            words = ['add', words[1], words[2], words[2]]
        elif words[0] == 'cmp':
            words = ['sub', registers[0], words[1], words[2]]
        elif words[0] == 'cpy':
            words = ['add', words[1], words[2], registers[0]]
        elif (words[0] in ['dec', 'inc'] and len(words) == 2):
            words = [words[0], words[1], words[1]]
        elif words[0] == 'jmp':
            words = ['bif', 'always', words[1]]
        elif words[0] == 'adc':
            words[0] = 'add'
            words.append('with_carry')
        elif words[0] == 'sbc':
            words[0] = 'sub'
            words.append('with_carry')
        original = words

        # begin machine code translation
        opcode = words[0]
        instruction = (symbols[opcode] << 12)
        words = [resolve(word) for word in words]

        if opcode in ['add', 'sub', 'xor', 'orr', 'and', 'inc', 'dec', 'rsh', 'ldi', 'lod']: # Reg Dest
            instruction |= (words[1] << 9)
        elif opcode in ['str']:
            instruction |= (words[1] << 3)

        if opcode in ['add', 'sub', 'xor', 'orr', 'and', 'inc', 'dec', 'rsh', 'str']: # Reg A
            instruction |= words[2]

        if opcode in ['add', 'sub', 'xor', 'orr', 'and']: # Reg B
            instruction |= (words[3] << 3 )

        if opcode in ['add', 'sub'] and len(words) == 5:
            instruction |= (words[4] << 8 )

        if opcode in ['ldi']: # Immediate
            instruction |= words[2]

        if opcode in ['bif']:
            instruction |= (words[1] << 9)
            instruction |= (words[2] << 2)

        as_string = bin(instruction)[2:].rjust(16, '0')
        machine_code.append(instruction >> 8 & 0xff)
        machine_code.append(instruction & 0xff)
        print(f"{index:02x}".upper(),'\t', as_string[:4], as_string[4:8], as_string[8:16], " ".join(original))
    
    machine_code_file.write(machine_code)
    machine_code_file.close()