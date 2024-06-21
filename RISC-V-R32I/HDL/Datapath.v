module Datapath #(parameter WIDTH=32)
(
    input clk, reset, 
    input  ALUSrc, ALUSrc_A, RegWrite, MemWrite, ResultSrc, SrcB_0Select,
    input WD3Sel, shamtMuxSelect,
    input [1:0] ShifterControl,PCSrc,
    input [3:0] ALUControl,
	 input [2:0] InstructionType,MemoryOutExtenderSelect,MemoryInExtenderSelect,ImmSrc,
    input [4:0] Debug_Source_select,
    output [31:0] Debug_output, PC, 
	 output [2:0] funct3,
	 output [6:0] funct7, op,
    output Zero, Negative, Carry,
	 output [6:0] Imm
);

wire [31:0] PCTarget, PCPlus4, PCNext, Instr;
assign funct3 = Instr[14:12];
assign funct7 = Instr[31:25];
assign op = Instr[6:0];
assign Imm = Instr[31:25];

Mux_4to1 #(.WIDTH(32)) PCRegInMux ( //
    .select(PCSrc),
    .input_0(PCPlus4),
    .input_1(PCTarget),
    .input_2(ALUResult),
    .input_3(31),
    .output_value(PCNext)
);

//wire [31:0] PC; outputta tanımlıyken içeri alabiliyoz mu emin değilim buna bakmak lazım quartus yok

Register_reset #(.WIDTH(32)) PCReg ( //
   .clk(clk), 
   .reset(reset),
	.DATA(PCNext),
	.OUT(PC)

);

Adder #(.WIDTH(WIDTH)) PCRegOutAdder ( //
    .DATA_A(PC),
    .DATA_B(4),
    .OUT(PCPlus4)
);

Instruction_memory #(.BYTE_SIZE(4), .ADDR_WIDTH(32)) Instruction_Memory ( //
    .ADDR(PC),
    .RD(Instr)
);  

wire [31:0] Result, RD1, RD2;
wire [31:0] WD3;

Mux_2to1 #(.WIDTH(32)) WD3Mux ( //
    .select(WD3Sel),
    .input_0(Result),
    .input_1(PCPlus4),
    .output_value(WD3)
);

Register_file #(.WIDTH(32)) Reg_file ( //
    .clk(clk), 
    .write_enable(RegWrite), 
    .reset(1'b0),
    .Source_select_0(Instr[19:15]), 
    .Source_select_1(Instr[24:20]), 
    .Debug_Source_select(Debug_Source_select), 
    .Destination_select(Instr[11:7]),
    .DATA(WD3), 
    .out_0(RD1), 
    .out_1(RD2), 
    .Debug_out(Debug_output)                                                    
);

wire [31:0] ImmExt;

Extender#(.WIDTH(32)) extender( //
    .select(ImmSrc),
    .DATA(Instr),
    .Extended_data(ImmExt),
    .instruction_type(InstructionType)
);

wire [31:0] SrcB;
wire [31:0] SrcA;
wire [31:0] ShifterOut,SrcB_0Out;
wire [31:0] WriteData = SrcB_0Out;
wire [4:0] ShifterShamt;

Mux_2to1 #(.WIDTH(5)) shamtMux ( //
    .select(shamtMuxSelect),
    .input_0(RD2[4:0]),
    .input_1(ImmExt[4:0]),
    .output_value(ShifterShamt)
);

shifter #(.WIDTH(32)) Shifter(//
    .control(ShifterControl),
    .shamt(ShifterShamt),	
    .DATA(RD1),	 
    .OUT(ShifterOut)
);

Mux_2to1 #(.WIDTH(32)) SrcB_0OutMux (//
    .select(SrcB_0Select),
    .input_0(RD2),
    .input_1(ShifterOut),
    .output_value(SrcB_0Out)
);

Mux_2to1 #(.WIDTH(32)) SrcAMux (//
    .select(ALUSrc_A),
    .input_0(RD1),
    .input_1(PC),
    .output_value(SrcA)
);

Mux_2to1 #(.WIDTH(32)) SrcBMux (//
    .select(ALUSrc),
    .input_0(SrcB_0Out),
    .input_1(ImmExt),
    
    .output_value(SrcB)
);

wire [31:0] ALUResult;
wire ALU_N, ALU_OVF;

ALU #(.WIDTH(32)) Almighty_ALU(//
    .control(ALUControl),
    .DATA_A(SrcA),
    .DATA_B(SrcB),
    .OUT(ALUResult),
    .CO(Carry),
    .OVF(ALU_OVF),
    .N(Negative),
    .Z(Zero)

);

Adder #(.WIDTH(WIDTH)) PCTargetAdder (//
    .DATA_A(PC),
    .DATA_B(ImmExt),
    .OUT(PCTarget)
);

wire [31:0] ReadData;

Memory #(.BYTE_SIZE(4), .ADDR_WIDTH(32)) Data_Memory(//
    .clk(clk),
    .WE(MemWrite),
    .ADDR(ALUResult),
    .WD(MemoryAddrIn),
    .RD(ReadData) 
);

wire [31:0] MemoryReadOut;
wire [31:0] MemoryAddrIn;

Extender #(.WIDTH(32)) MemoryInExtender(//
    .select(MemoryInExtenderSelect),
    .DATA(WriteData),
    .Extended_data(MemoryAddrIn),
    .instruction_type(3'd5)
);

Extender #(.WIDTH(32)) MemoryOutExtender(//
    .select(MemoryOutExtenderSelect),
    .DATA(ReadData),
    .Extended_data(MemoryReadOut),
    .instruction_type(3'd5)
);

Mux_2to1 #(.WIDTH(32)) ResultMux(//
    .select(ResultSrc),
    .input_0(ALUResult),
    .input_1(MemoryReadOut),
    .output_value(Result)
);

endmodule