module computer (
    input clk,
    input reset,
    input [4:0] debug_reg_select,
    output [31:0] debug_reg_out,
    output [31:0] fetchPC
);

wire ResultSrc, RegWrite, MemWrite, ALUSrc, ALUSrc_A, SrcB_0Select, shamtMuxSelect, WD3Sel, ShifterMux, Zero, Negative, Carry;
wire [1:0] ShifterControl,PCSrc;
wire [2:0] ImmSrc, MemoryOutExtenderSelect, MemoryInExtenderSelect, InstructionType, funct3;
wire [3:0] ALUControl;
wire [6:0] op, funct7, Imm;


Control_unit Control_unit(
    .op                     (op),
    .funct3                 (funct3),
    .funct7                 (funct7), 
    .Zero                   (Zero), 
    .Negative               (Negative),
    .WD3Sel                 (WD3Sel),
    .PCSrc                  (PCSrc), 
    .ResultSrc              (ResultSrc), 
    .RegWrite               (RegWrite), 
    .MemWrite               (MemWrite), 
    .ALUSrc                 (ALUSrc), 
    .ALUSrc_A               (ALUSrc_A),   
    .SrcB_0Select           (SrcB_0Select),
    .shamtMuxSelect         (shamtMuxSelect),
    .ALUControl             (ALUControl),
    .ShifterControl         (ShifterControl),
    .ImmSrc                 (ImmSrc), 
    .MemoryOutExtenderSelect(MemoryOutExtenderSelect), 
    .MemoryInExtenderSelect (MemoryInExtenderSelect),
    .InstructionType        (InstructionType),
	.Imm                    (Imm),
    .Carry                  (Carry)
);


Datapath Datapath(
    .clk                    (clk), 
    .reset                  (reset), 
    .ALUSrc                 (ALUSrc), 
    .ALUSrc_A               (ALUSrc_A), 
    .RegWrite               (RegWrite), 
    .MemWrite               (MemWrite), 
    .ResultSrc              (ResultSrc), 
    .SrcB_0Select           (SrcB_0Select),
    .WD3Sel                 (WD3Sel), 
    .shamtMuxSelect         (shamtMuxSelect),
    .MemoryOutExtenderSelect(MemoryOutExtenderSelect),
    .MemoryInExtenderSelect (MemoryInExtenderSelect),
    .ImmSrc                 (ImmSrc),
    .ShifterControl         (ShifterControl),
    .PCSrc                  (PCSrc),
    .ALUControl             (ALUControl),
    .InstructionType        (InstructionType),
    .Debug_Source_select    (debug_reg_select),
    .Debug_output           (debug_reg_out),
    .Zero                   (Zero), 
    .Negative               (Negative),
    .PC                     (fetchPC),
	 .funct3                 (funct3),
	 .funct7                 (funct7),
	 .op                     (op),
	 .Imm                    (Imm),
     .Carry                  (Carry)
);

endmodule
