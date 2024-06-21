import Helper_lib

def format_signed_binary(imm, bit_width):
    if imm < 0:
        # Calculate two's complement
        imm = (1 << bit_width) + imm
    return format(imm, f'0{bit_width}b')

def generate_risc_v_instruction(instruction, rd=None, rs1=None, rs2=None, imm=None):
    instruction_set = {
        'LW':  {'type': 'I', 'opcode': '0000011', 'funct3': '010'},
        'LH':  {'type': 'I', 'opcode': '0000011', 'funct3': '001'},
        'LHU': {'type': 'I', 'opcode': '0000011', 'funct3': '101'},
        'LB':  {'type': 'I', 'opcode': '0000011', 'funct3': '000'},
        'LBU': {'type': 'I', 'opcode': '0000011', 'funct3': '100'},
        'SW':  {'type': 'S', 'opcode': '0100011', 'funct3': '010'},
        'SH':  {'type': 'S', 'opcode': '0100011', 'funct3': '001'},
        'SB':  {'type': 'S', 'opcode': '0100011', 'funct3': '000'},
        'LUI': {'type': 'U', 'opcode': '0110111'},
        'AUIPC': {'type': 'U', 'opcode': '0010111'},
        'XORID': {'type': 'I', 'opcode': '0010011', 'funct3': '100'},
        'ADD': {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0000000'},
        'ADDI': {'type': 'I', 'opcode': '0010011', 'funct3': '000'},
        'SUB': {'type': 'R', 'opcode': '0110011', 'funct3': '000', 'funct7': '0100000'},
        'AND': {'type': 'R', 'opcode': '0110011', 'funct3': '111', 'funct7': '0000000'},
        'ANDI': {'type': 'I', 'opcode': '0010011', 'funct3': '111'},
        'OR': {'type': 'R', 'opcode': '0110011', 'funct3': '110', 'funct7': '0000000'},
        'ORI': {'type': 'I', 'opcode': '0010011', 'funct3': '110'},
        'XOR': {'type': 'R', 'opcode': '0110011', 'funct3': '100', 'funct7': '0000000'},
        'XORI': {'type': 'I', 'opcode': '0010011', 'funct3': '100'},
        'SLL': {'type': 'R', 'opcode': '0110011', 'funct3': '001', 'funct7': '0000000'},
        'SLLI': {'type': 'I', 'opcode': '0010011', 'funct3': '001'},
        'SRL': {'type': 'R', 'opcode': '0110011', 'funct3': '101', 'funct7': '0000000'},
        'SRLI': {'type': 'I', 'opcode': '0010011', 'funct3': '101'},
        'SRA': {'type': 'R', 'opcode': '0110011', 'funct3': '101', 'funct7': '0100000'},
        'SRAI': {'type': 'I', 'opcode': '0010011', 'funct3': '101'},
        'SLT': {'type': 'R', 'opcode': '0110011', 'funct3': '010', 'funct7': '0000000'},
        'SLTI': {'type': 'I', 'opcode': '0010011', 'funct3': '010'},
        'SLTU': {'type': 'R', 'opcode': '0110011', 'funct3': '011', 'funct7': '0000000'},
        'SLTIU': {'type': 'I', 'opcode': '0010011', 'funct3': '011'},
        'BEQ': {'type': 'B', 'opcode': '1100011', 'funct3': '000'},
        'BNE': {'type': 'B', 'opcode': '1100011', 'funct3': '001'},
        'BLT': {'type': 'B', 'opcode': '1100011', 'funct3': '100'},
        'BGE': {'type': 'B', 'opcode': '1100011', 'funct3': '101'},
        'BLTU': {'type': 'B', 'opcode': '1100011', 'funct3': '110'},
        'BGEU': {'type': 'B', 'opcode': '1100011', 'funct3': '111'},
        'JAL': {'type': 'J', 'opcode': '1101111'},
        'JALR': {'type': 'I', 'opcode': '1100111', 'funct3': '000'},
        'XORID' : {'type' : 'I', 'opcode': '0001011', 'funct3': '000'},
    }
    
    if instruction not in instruction_set:
        raise ValueError(f"Unsupported instruction: {instruction}")
    
    instr_data = instruction_set[instruction]
    instr_type = instr_data['type']
    opcode = instr_data['opcode']
    
    if instr_type == 'R':
        if rd is None or rs1 is None or rs2 is None:
            raise ValueError("R-type instructions require rd, rs1, and rs2")
        funct3 = instr_data['funct3']
        funct7 = instr_data['funct7']
        instruction_bin = funct7 + format(rs2, '05b') + format(rs1, '05b') + funct3 + format(rd, '05b') + opcode
    
    elif instr_type == 'I':
        if rd is None or rs1 is None or imm is None:
            raise ValueError("I-type instructions require rd, rs1, and imm")
        funct3 = instr_data['funct3']
        instruction_bin = format_signed_binary(imm, 12) + format(rs1, '05b') + funct3 + format(rd, '05b') + opcode

        if(instruction == "SRAI"):
            instruction_bin = format_signed_binary(imm, 12)[0] + '1' + format_signed_binary(imm, 12)[2:] + format(rs1, '05b') + funct3 + format(rd, '05b') + opcode

    elif instr_type == 'S':
        if rs1 is None or rs2 is None or imm is None:
            raise ValueError("S-type instructions require rs1, rs2, and imm")
        funct3 = instr_data['funct3']
        imm_bin = format_signed_binary(imm, 12)
        instruction_bin = imm_bin[:7] + format(rs2, '05b') + format(rs1, '05b') + funct3 + imm_bin[7:] + opcode
    
    elif instr_type == 'B':
        if rs1 is None or rs2 is None or imm is None:
            raise ValueError("B-type instructions require rs1, rs2, and imm")
        funct3 = instr_data['funct3']
        imm_bin = format_signed_binary(imm << 1, 13)
        instruction_bin = imm_bin[0] + imm_bin[2:8] + format(rs2, '05b') + format(rs1, '05b') + funct3 + imm_bin[8:12] + imm_bin[1] + opcode
    
    elif instr_type == 'U':
        if rd is None or imm is None:
            raise ValueError("U-type instructions require rd and imm")
        instruction_bin = format_signed_binary(imm, 20) + format(rd, '05b') + opcode
    
    elif instr_type == 'J':
        if rd is None or imm is None:
            raise ValueError("J-type instructions require rd and imm")
        imm_bin = format_signed_binary(imm, 21)
        instruction_bin = imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + format(rd, '05b') + opcode
    
    else:
        raise ValueError(f"Unsupported instruction type: {instr_type}")
    
    instruction_hex = hex(int(instruction_bin, 2))[2:].zfill(8)
    return instruction_hex

# # Arithmetic Instructions
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ADDI', rd=1, rs1=0, imm=-5)))       # x1 = x0 + -5
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ADD', rd=2, rs1=1, rs2=1)))         # x2 = x1 + x1
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SUB', rd=3, rs1=1, rs2=2)))         # x3 = x1 - x2
# 
# # Logic Instructions
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('OR', rd=4, rs1=3, rs2=2)))          # x4 = x3 | x2
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('AND', rd=5, rs1=4, rs2=2)))         # x5 = x4 & x2
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('XOR', rd=6, rs1=5, rs2=4)))         # x6 = x5 ^ x4
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ORI', rd=7, rs1=4, imm=250)))       # x7 = x4 | 250
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ANDI', rd=8, rs1=7, imm=-200)))     # x8 = x7 & -200
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('XORI', rd=9, rs1=8, imm=49)))       # x9 = x8 ^ 49
# 
# # Shift Intructions
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLL', rd=10, rs1=8, rs2=3)))        # x10 = x8 << x3
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SRL', rd=11, rs1=8, rs2=3)))        # x11 = x8 >> x3
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SRA', rd=12, rs1=8, rs2=3)))        # x12 = x8 >>> x3
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLLI', rd=10, rs1=8, imm=5)))       # x10 = x8 << 5
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SRLI', rd=11, rs1=8, imm=5)))       # x11 = x8 >> 5
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SRAI', rd=12, rs1=8, imm=5)))       # x12 = x8 >>> 5
# 
# # Set if less than
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLT',   rd=13, rs1=4, rs2=3)))      # set x13 to 1 if x4 < x3
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLTI',  rd=14, rs1=4, imm=5)))      # set x14 to 1 if x4 < -9
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLTU',  rd=15, rs1=4, rs2=3)))      # set x15 to 1 if x4 < x3
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SLTIU', rd=16, rs1=4, imm=5)))      # set x16 to 1 if x4 < -9
# 
# # Conditional Branch
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BLT' , rs1=13, rs2=14, imm=40)))    # if (x13 < x14) jump 40
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BGE' , rs1=12, rs2=13, imm=40)))    # if (x12 >= x13) jump 40
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BLTU', rs1=13, rs2=13, imm=40)))    # if (x10 < x1) jump 4
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BGEU', rs1=0, rs2=3, imm=40)))      # if (x12 >= x1) jump 4
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BNE' , rs1=13, rs2=14, imm=8)))     # if (x13 != x14) jump 16
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('BEQ' , rs1=13, rs2=14, imm=4)))     # if (x1 == x31) jump 8
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ADDI', rd=1, rs1=0, imm=-5)))       # x1 = x0 + -5
# 
# # Unconditional Jump
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('JALR', rd=13, rs1=0, imm=92)))      # jump 94 + x0, set x13 to the next instruction
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('JAL',  rd=15, imm=4)))              # jump 4, set x15 to the next instruction
# 
# # Store
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SW', rs1=3, rs2=12, imm=10)))       # store word from x12 to memory address x2 + 10
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SH', rs1=3, rs2=12, imm=20)))       # store halfword from x12 to memory address x3 + 20
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SB', rs1=3, rs2=12, imm=30)))       # store byte from x12 to memory address x3 + 30
#    
# # Load   
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LW',  rd=16, rs1=3, imm=10)))       # load word from memory address x2 + 100 to x2
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LH',  rd=17, rs1=3, imm=20)))       # load halfword from memory address x2 + 0 to x4
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LHU', rd=18, rs1=3, imm=20)))       # load unsigned halfword from memory address x2 + 0 to x6
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LB',  rd=19, rs1=3, imm=30)))       # load byte from memory address x2 + 0 to x8
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LBU', rd=20, rs1=3, imm=30)))       # load unsigned byte from memory address x2 + 0 to x10
# 
# # Others
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('LUI', rd=21, imm=3)))               # load upper immediate 3 to x21
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('AUIPC', rd=22, imm=3)))             # add upper immediate pc-relative 1 to x19
# 
# # Extra Instruction
# print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('XORID', rd=23, imm=1, rs1=1)))      # XOR student id's

#print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ADDI', rd=1, rs1=0, imm=-5)))       # x1 = x0 + -5
#print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('ADD', rd=2, rs1=1, rs2=1)))         # x2 = x1 + x1
#print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('SUB', rd=3, rs1=1, rs2=2)))         # x3 = x1 - x2
#print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('JAL',  rd=15, imm=-12)))

print(Helper_lib.reverse_hex_string_endiannes(generate_risc_v_instruction('JAL',  rd=0, imm=-12)))