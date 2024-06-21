# ==============================================================================
# Authors:              Doğu Erkan Arkadaş
#
# Cocotb Testbench:     For Single Cycle ARM Laboratory
#
# Description:
# ------------------------------------
# Test bench for the single cycle laboratory, used by the students to check their designs
#
# License:
# ==============================================================================
class Constants:
    # Define your constant values as class attributes for operation types
    ADD = 4
    SUB = 2
    AND = 0
    ORR = 12
    CMP = 10
    MOV = 13
    EQ = 0
    NE = 1
    AL = 14

import logging
import cocotb
from Helper_lib import read_file_to_list,Instruction,rotate_right, shift_helper, ByteAddressableMemory,reverse_hex_string_endiannes, get_signed_magnitude
from Helper_Student import Log_Datapath,Log_Controller
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Edge, Timer
from cocotb.binary import BinaryValue

def to_unsigned_32bit(value):
    bit_width = 32
    # Mask the value to fit within 32 bits
    mask = (1 << bit_width) - 1
    return value & mask

def lsr(value, shift, bit_width):
    # Mask to ensure the value fits within the bit-width before shifting
    mask = (1 << bit_width) - 1
    value &= mask

    # Perform the logical right shift
    value >>= shift

    # Mask again to ensure the value fits within the bit-width after shifting
    value &= mask >> shift

    return value

def sra(value, shift, bit_width):
    if value < 0:
        # For negative values, create the two's complement representation and perform the shift
        value = (value + (1 << bit_width))
        value >>= shift
        # Preserve the sign bit after the shift
        value |= ((1 << shift) - 1) << (bit_width - shift)
    else:
        # For positive values, perform a simple right shift
        value >>= shift

    # Mask to ensure the value fits within the bit-width
    mask = (1 << bit_width) - 1
    return value & mask

class TB:
    def __init__(self, Instruction_list,dut,dut_PC,dut_regfile):
        self.dut = dut
        self.dut_PC = dut_PC
        self.dut_regfile = dut_regfile
        self.Instruction_list = Instruction_list
        #Configure the logger
        self.logger = logging.getLogger("Performance Model")
        self.logger.setLevel(logging.DEBUG)
        #Initial values are all 0 as in a FPGA
        self.PC = 0
        self.Z_flag = 0
        self.Register_File =[]
        for i in range(32):
            self.Register_File.append(0)
        #Memory is a special class helper lib to simulate HDL counterpart    
        self.memory = ByteAddressableMemory(1024)

        self.clock_cycle_count = 0        
          
    #Calls user populated log functions    
    def log_dut(self):
        Log_Datapath(self.dut,self.logger)
        Log_Controller(self.dut,self.logger)

    #Compares and lgos the PC and register file of Python module and HDL design
    def compare_result(self):
        self.logger.debug("************* Performance Model / DUT Data  **************")
        self.logger.debug("PC:%08X \t PC:%08X",self.PC,self.dut_PC.value.integer)
        for i in range(32):
            self.logger.debug("Register%d: %08X \t %08X",i,to_unsigned_32bit(self.Register_File[i]), self.dut_regfile.Reg_Out[i].value.integer)
        assert self.PC == self.dut_PC.value
        for i in range(32):
           assert to_unsigned_32bit(self.Register_File[i]) == self.dut_regfile.Reg_Out[i].value.integer
        
    #Function to write into the register file, handles writing into R15(PC)
    def write_to_register_file(self,register_no, data):
        self.Register_File[register_no] = data

    #A model of the verilog code to confirm operation, data is In_data
    def performance_model(self):
        self.logger.debug("**************** Clock cycle: %d **********************", self.clock_cycle_count)
        self.clock_cycle_count += 1

        # Read current instructions, extract and log the fields
        self.logger.debug("**************** Instruction No: %d **********************", int((self.PC) / 4))
        current_instruction = self.Instruction_list[int((self.PC) / 4)]
        current_instruction = current_instruction.replace(" ", "")
        
        # We need to reverse the order of bytes since little endian makes the string reversed in Python
        current_instruction = reverse_hex_string_endiannes(current_instruction)
        
        # Initial PC increment for next instruction
        self.PC += 4
        
        # Flag to check if the current instruction will be executed.
        execute_flag = True
        
        # Call Instruction calls to get each field from the instruction
        inst_fields = Instruction(current_instruction)
        inst_fields.log(self.logger)
        
        # Determine the operation type and execute
        binary_instr = format(int(current_instruction, 16), '032b')
        opcode = binary_instr[25:32]

        if execute_flag:
            if opcode in ['0110011']:  # R-type
                rs1 = int(binary_instr[12:17], 2)
                rs2 = int(binary_instr[7:12], 2)
                rd = int(binary_instr[20:25], 2)
                funct3 = binary_instr[17:20]
                funct7 = binary_instr[0:7]
                
                if funct3 == '000' and funct7 == '0000000':
                    datap_result = self.Register_File[rs1] + self.Register_File[rs2]
                    self.write_to_register_file(rd, datap_result)  # ADD
                elif funct3 == '000' and funct7 == '0100000':
                    datap_result = self.Register_File[rs1] - self.Register_File[rs2]
                    self.write_to_register_file(rd, datap_result)  # SUB
                elif funct3 == '111':
                    datap_result = self.Register_File[rs1] & self.Register_File[rs2]
                    self.write_to_register_file(rd, datap_result)  # AND
                elif funct3 == '110':
                    datap_result = self.Register_File[rs1] | self.Register_File[rs2]
                    self.write_to_register_file(rd, datap_result)  # OR
                elif funct3 == '100':
                    datap_result = self.Register_File[rs1] ^ self.Register_File[rs2]
                    self.write_to_register_file(rd, datap_result)  # XOR
                elif funct3 == '001' and funct7 == '0000000':      
                    datap_result = self.Register_File[rs1] << (self.Register_File[rs2] & 0x1F)
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SLL
                elif funct3 == '101' and funct7 == '0000000':      
                    datap_result = lsr(self.Register_File[rs1], self.Register_File[rs2] & 0x1F, 32)
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SRL
                elif funct3 == '101' and funct7 == '0100000':
                    datap_result = sra(self.Register_File[rs1], (self.Register_File[rs2] & 0x1F), 32)
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SRA
                elif funct3 == '010' and funct7 == '0000000':
                    if(self.Register_File[rs1] < self.Register_File[rs2]):
                        self.write_to_register_file(rd, 1)  # SLT
                elif funct3 == '011' and funct7 == '0000000':
                    if(to_unsigned_32bit(self.Register_File[rs1]) < to_unsigned_32bit(self.Register_File[rs2])):
                        self.write_to_register_file(rd, 1)  # SLTU
                else:
                    self.logger.error("Not supported R-type instruction!")
                    assert False

            elif opcode in ['0010011']:  # I-type
                rs1 = int(binary_instr[12:17], 2)
                rd = int(binary_instr[20:25], 2)
                imm = get_signed_magnitude(int(binary_instr[0:12], 2), 12)
                funct3 = binary_instr[17:20]

                if funct3 == '000':
                    datap_result = self.Register_File[rs1] + imm
                    self.write_to_register_file(rd, datap_result)  # ADDI
                elif funct3 == '111':
                    datap_result = self.Register_File[rs1] & imm
                    self.write_to_register_file(rd, datap_result)  # ANDI
                elif funct3 == '110':
                    datap_result = self.Register_File[rs1] | imm
                    self.write_to_register_file(rd, datap_result)  # ORI
                elif funct3 == '100':
                    datap_result = self.Register_File[rs1] ^ imm
                    self.write_to_register_file(rd, datap_result)  # XORI
                elif funct3 == '001':
                    datap_result = self.Register_File[rs1] << imm
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SLLI
                elif funct3 == '101' and binary_instr[1] != '1':
                    datap_result = lsr(self.Register_File[rs1], imm, 32)
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SRLI
                elif funct3 == '101' and binary_instr[1] == '1':
                    imm = get_signed_magnitude(int(binary_instr[7:12], 2), 12)
                    datap_result = sra(self.Register_File[rs1], imm, 32)
                    self.write_to_register_file(rd, get_signed_magnitude(datap_result, 32))  # SRAI
                elif funct3 == '010':
                    if(self.Register_File[rs1] < imm):
                        self.write_to_register_file(rd, 1)  # SLTI
                elif funct3 == '011':
                    if(to_unsigned_32bit(self.Register_File[rs1]) < to_unsigned_32bit(imm)):
                        self.write_to_register_file(rd, 1)  # SLTIU
                else:
                    self.logger.error("Not supported I-type instruction!")
                    self.logger.debug("Funcr3: %s", funct3)
                    assert False
            
            elif opcode in ['0100011']:  # S-type
                rs1 = int(binary_instr[12:17], 2)
                rs2 = int(binary_instr[7:12], 2)
                imm = get_signed_magnitude((int(binary_instr[0:7], 2) << 5) + int(binary_instr[20:25], 2), 12)
                funct3 = binary_instr[17:20]
                
                if funct3 == '010':
                    self.memory.write(self.Register_File[rs1] + imm, to_unsigned_32bit(self.Register_File[rs2]))  # SW
                elif funct3 == '001':
                    self.memory.write(self.Register_File[rs1] + imm, to_unsigned_32bit(self.Register_File[rs2]) & 0xFFFF) # SH
                elif funct3 == '000':
                    self.memory.write(self.Register_File[rs1] + imm, to_unsigned_32bit(self.Register_File[rs2]) & 0xFF) # SB
                else:
                    self.logger.error("Not supported S-type instruction!")
                    assert False

            elif opcode in ['0000011']:  # Load Instructions
                rs1 = int(binary_instr[12:17], 2)
                rd = int(binary_instr[20:25], 2)
                imm = get_signed_magnitude(int(binary_instr[0:12], 2), 12)
                funct3 = binary_instr[17:20]

                if funct3 == '010':
                    self.write_to_register_file(rd, get_signed_magnitude(int.from_bytes(self.memory.read(self.Register_File[rs1] + imm)), 32))  # LW
                elif funct3 == '001':
                    self.write_to_register_file(rd, get_signed_magnitude(int.from_bytes(self.memory.read(self.Register_File[rs1] + imm)) & 0xFFFF, 16))  # LH
                elif funct3 == '101':
                    self.write_to_register_file(rd, (int.from_bytes(self.memory.read(self.Register_File[rs1] + imm))) & 0xFFFF)  # LHU
                elif funct3 == '000':
                    self.write_to_register_file(rd, get_signed_magnitude(int.from_bytes(self.memory.read(self.Register_File[rs1] + imm)) & 0xFF, 8))  # LB
                elif funct3 == '100':
                    self.write_to_register_file(rd, (int.from_bytes(self.memory.read(self.Register_File[rs1] + imm))) & 0xFF)  # LBU
                else:
                    self.logger.error("Not supported load instruction!")
                    assert False

            elif opcode in ['1100011']:  # B-type (conditional branch)  
                rs1 = int(binary_instr[12:17], 2)
                rs2 = int(binary_instr[7:12], 2)
                imm_temp = 0
                imm_temp = (int(binary_instr[0], 2) << 12) | (int(binary_instr[24], 2) << 11) | (int(binary_instr[1:7], 2) << 5) | (int(binary_instr[20:24], 2) << 1)
                imm = get_signed_magnitude(imm_temp, 12)
                funct3 = binary_instr[17:20]

                if funct3 == '000':
                    if self.Register_File[rs1] == self.Register_File[rs2]:
                        self.PC += imm  # BEQ
                        self.PC -= 4
                elif funct3 == '001':
                    if self.Register_File[rs1] != self.Register_File[rs2]:
                        self.PC += imm  # BNE
                        self.PC -= 4
                elif funct3 == '100':
                    if self.Register_File[rs1] < self.Register_File[rs2]:
                        self.PC += imm  # BLT
                        self.PC -= 4
                elif funct3 == '101':
                    if self.Register_File[rs1] >= self.Register_File[rs2]:
                        self.PC += imm  # BGE
                        self.PC -= 4
                elif funct3 == '110':
                    if abs(self.Register_File[rs1]) < to_unsigned_32bit(self.Register_File[rs2]):
                        self.PC += imm  # BLTU
                        self.PC -= 4                                  
                elif funct3 == '111':
                    if abs(self.Register_File[rs1]) >= to_unsigned_32bit(self.Register_File[rs2]):
                        self.PC += imm  # BGEU
                        self.PC -= 4                  
                else:
                    self.logger.error("Not supported B-type instruction!")
                    assert False

            elif opcode in ['1101111']:  # J-type (jump)
                self.PC -= 4
                rd = int(binary_instr[20:25], 2)
                imm_temp = (int(binary_instr[0:1], 2) << 20) + (int(binary_instr[12:20], 2) << 12) + (int(binary_instr[11:12], 2) << 11) | (int(binary_instr[1:11], 2) << 1)
                imm = get_signed_magnitude(imm_temp, 21)
                if(rd != 0):
                    self.write_to_register_file(rd, self.PC + 4)
                self.PC += imm  # JAL

            elif opcode in ['1100111']: # JALR
                self.PC -= 4
                rs1 = int(binary_instr[12:17], 2)
                rd = int(binary_instr[20:25], 2)
                imm = get_signed_magnitude(int(binary_instr[0:12], 2), 12)
                rs1_value = self.Register_File[rs1]
                self.write_to_register_file(rd, self.PC + 4)                
                self.PC = imm + rs1_value

            elif opcode in ['0110111']: # LUI
                rd = int(binary_instr[20:25], 2)
                imm = int(binary_instr[0:20], 2)
                self.write_to_register_file(rd, imm << 12)
            
            elif opcode in ['0010111']: # AUPIC
                rd = int(binary_instr[20:25], 2)
                imm = int(binary_instr[0:20], 2)
                self.write_to_register_file(rd, self.PC - 4 + (imm << 12))
            
            elif opcode in ['0001011']: # XORID
                rs1 = int(binary_instr[12:17], 2)
                rd = int(binary_instr[20:25], 2)
                imm = int(binary_instr[0:12], 2)
                funct3 = binary_instr[17:20]

                self.write_to_register_file(rd, (self.Register_File[rs1] ^ (2442986 ^ 2442390)))
                
            else:
                self.logger.error("Invalid opcode!")
                assert False
        else:
            self.logger.debug("Current Instruction is not executed")

    async def run_test(self):
        self.performance_model()
        #Wait 1 us the very first time bc. initially all signals are "X"
        await Timer(1, units="us")
        self.log_dut()
        await RisingEdge(self.dut.clk)
        await FallingEdge(self.dut.clk)
        self.compare_result()
        while(int(self.Instruction_list[int((self.PC)/4)].replace(" ", ""),16)!=0):
            self.performance_model()
            #Log datapath and controller before clock edge, this calls user filled functions
            self.log_dut()
            await RisingEdge(self.dut.clk)
            await FallingEdge(self.dut.clk)
            self.compare_result()
            input()
                
                   
@cocotb.test()
async def Single_cycle_test(dut):
    #Generate the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Reset onces before continuing with the tests
    dut.reset.value=1
    await RisingEdge(dut.clk)
    dut.reset.value=0
    await FallingEdge(dut.clk)
    instruction_lines = read_file_to_list('Instructions.hex')
    #Give PC signal handle and Register File MODULE handle
    tb = TB(instruction_lines,dut, dut.fetchPC, dut.Datapath.Reg_file)
    await tb.run_test()