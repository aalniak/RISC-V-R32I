def read_file_to_list(filename):
    """
    Reads a text file and returns a list where each element is a line in the file.

    :param filename: The name of the file to read.
    :return: A list of strings, where each string is a line from the file.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Stripping newline characters from each line
        lines = [line.strip() for line in lines]
    return lines

class Instruction:
    """
    Parses a 32-bit RISC-V instruction in hexadecimal format.

    :param instruction: A string representing the 32-bit instruction in hex format.
    :return: This class with the fields parsed from the instruction.
    """
class Instruction:
    """
    Parses a 32-bit RISC-V instruction in hexadecimal format.

    :param instruction: A string representing the 32-bit instruction in hex format.
    :return: This class with the fields parsed from the instruction.
    """
    def __init__(self, instruction):
        # Convert the hex instruction to a 32-bit binary string
        self.binary_instr = format(int(instruction, 16), '032b')
        
        # Common fields across different types
        self.opcode = int(self.binary_instr[25:32], 2)  # Corrected the opcode extraction to bits 25 to 31
        
        # R-Type
        self.funct7 = self.binary_instr[0:7]  # Corrected to bits 0 to 6
        self.rs2 = int(self.binary_instr[7:12], 2)  # Corrected to bits 7 to 11
        self.rs1 = int(self.binary_instr[12:17], 2)  # Corrected to bits 12 to 16
        self.funct3 = self.binary_instr[17:20]  # Corrected to bits 17 to 19
        self.rd = int(self.binary_instr[20:25], 2)  # Corrected to bits 20 to 24
        
        # I-Type
        self.imm_I = int(self.binary_instr[0:12], 2)  # Immediate is from bits 0 to 11
        self.rs1_I = int(self.binary_instr[12:17], 2)  # rs1 is from bits 12 to 16
        self.funct3_I = self.binary_instr[17:20]  # funct3 is from bits 17 to 19
        self.rd_I = int(self.binary_instr[20:25], 2)  # rd is from bits 20 to 24

        # S-Type
        self.imm_S = (int(self.binary_instr[0:7], 2) << 5) + int(self.binary_instr[20:25], 2)
        self.rs1_S = int(self.binary_instr[12:17], 2)  # rs1 is from bits 12 to 16
        self.rs2_S = int(self.binary_instr[7:12], 2)  # rs2 is from bits 7 to 11
        self.funct3_S = self.binary_instr[17:20]  # funct3 is from bits 17 to 19

        # B-Type
        imm_temp = (int(self.binary_instr[0], 2) << 12) | (int(self.binary_instr[24], 2) << 11) | (int(self.binary_instr[1:7], 2) << 5) | (int(self.binary_instr[20:24], 2) << 1)
        self.imm_B = get_signed_magnitude(imm_temp, 12)
        self.rs1_B = int(self.binary_instr[12:17], 2)  # rs1 is from bits 12 to 16
        self.rs2_B = int
        
    def log(self, logger):
        logger.debug("****** Current Instruction *********")
        logger.debug("Binary string: %s", self.binary_instr)
        logger.debug("Opcode: %s", '{0:07b}'.format(self.opcode))
        
        if self.opcode in [51]:  # This is for R-type operations
            logger.debug("Operation type R-Type")
            logger.debug("Funct7: %s, RS2: %d, RS1: %d, Funct3: %s, RD: %d", self.funct7, self.rs2, self.rs1, self.funct3, self.rd)
        elif self.opcode in [3, 19]:  # This covers load and immediate type operations
            logger.debug("Operation type I-Type")
            logger.debug("Immediate: %d, RS1: %d, Funct3: %s, RD: %d", self.imm_I, self.rs1, self.funct3, self.rd)
        elif self.opcode in [35]:  # S-type
            logger.debug("Operation type S-Type")
            logger.debug("Immediate: %d, RS2: %d, RS1: %d, Funct3: %s", self.imm_S, self.rs2, self.rs1, self.funct3)
        elif self.opcode in [99]:  # B-type
            logger.debug("Operation type B-Type")
            logger.debug("Immediate: %d, RS2: %d, RS1: %d, Funct3: %s", self.imm_B, self.rs2, self.rs1, self.funct3)
        elif self.opcode in [55, 23]:  # U-type and UJ-type (for simplicity grouped together)
            logger.debug("Operation type U-Type or J-Type")
            logger.debug("RD: %d", self.rd)

        
def rotate_right(value, shift, n_bits=32):
    """
    Rotate `value` to the right by `shift` bits.

    :param value: The integer value to rotate.
    :param shift: The number of bits to rotate by.
    :param n_bits: The bit-width of the integer (default 32 for standard integer).
    :return: The value after rotating to the right.
    """
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    return (value >> shift) | (value << (n_bits - shift)) & ((1 << n_bits) - 1)

def shift_helper(value, shift,shift_type, n_bits=32):
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    match shift_type:
        case 0:
            return (value  << shift)% 0x100000000
        case 1:
            return (value  >> shift) % 0x100000000
        case 2:
            if((value & 0x80000000)!=0):
                    filler = (0xFFFFFFFF >> (n_bits-shift))<<((n_bits-shift))
                    return ((value  >> shift)|filler) % 0x100000000
            else:
                return (value  >> shift) % 0x100000000
        case 3:
            return rotate_right(value,shift,n_bits)
        
def reverse_hex_string_endiannes(hex_string):  
    reversed_string = bytes.fromhex(hex_string)
    reversed_string = reversed_string[::-1]
    reversed_string = reversed_string.hex()        
    return  reversed_string
class ByteAddressableMemory:
    def __init__(self, size):
        self.size = size
        self.memory = bytearray(size)  # Initialize memory as a bytearray of the given size

    def read(self, address):
        if address < 0 or address + 4 > self.size:
            raise ValueError("Invalid memory address or length")
        return_val = bytes(self.memory[address : address + 4])
        return_val = return_val[::-1]
        return return_val

    def write(self, address, data):
        if address < 0 or address + 4> self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(4, byteorder='little')
        self.memory[address : address + 4] = data_bytes

def get_signed_magnitude(binary_value, bit_width):
    value = int(binary_value)
    if value >= 2**(bit_width - 1):
        value -= 2**bit_width
    return value
