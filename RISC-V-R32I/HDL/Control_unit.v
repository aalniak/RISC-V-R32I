module Control_unit(
	input [6:0] op,
	input [6:0] Imm,
	input [2:0] funct3,
    input [6:0] funct7, // a single bit Instr[30] is enough to resolve the type, but lets go with a structured fashion
	input  Carry, Zero, Negative,
	output reg WD3Sel,
	output reg ResultSrc, RegWrite, MemWrite, ALUSrc, ALUSrc_A, SrcB_0Select,shamtMuxSelect,
	output reg [3:0] ALUControl,
	output reg [1:0] ShifterControl,PCSrc,
    output reg [2:0] ImmSrc, MemoryOutExtenderSelect, MemoryInExtenderSelect,InstructionType

);
wire funct7_6 = funct7[5];
always@(*) begin
    ShifterControl = {funct7_6,funct3[2]}; // Is correct, trust me.
    MemoryOutExtenderSelect = funct3;  // Is correct, trust me.
    MemoryInExtenderSelect = funct3; //Same mapping as MemoryOutExtenderSelect
    case (op)
    // R-Type Instructions: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU
    7'b0110011: begin 
        ALUControl = {funct3,funct7_6};
        WD3Sel = 0;       //Register file WD3 is Result
        ALUSrc_A = 0;     //SrcA = RD1;
        InstructionType = 0; //Avoid latches
        RegWrite = 1;  // All instructions trigger a register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 0;    // Takes data from RD2, not extended Immediate 
        PCSrc = 0;     // No jumps taken, should go with regular PC+4
        ImmSrc = 0;    // Should not matter, to avoid latches
        ResultSrc = 0; // Takes the data from ALUResult
        shamtMuxSelect = 0;  //Register for shifter shamt in
        if (funct3 == 3'b101 | funct3 == 3'b001) begin //Is a shift instruction
            SrcB_0Select = 1;
        end
        else begin
            //Set less than is already implemented in ALU with ALUControl and SrcB_0Select=0.
            SrcB_0Select = 0;
        end
    end

    // I-Type Instructions: ADDI, ANDI, ORI, XORI, SLLI, SRLI, SRAI, SLTI, SLTIU, 
    7'b0010011: begin 
		  if (funct3==3'b001 | funct3==3'b101)
		      ALUControl = {funct3,Imm[5]};
		  else 
		      ALUControl = {funct3,1'b0};
		  
        ALUControl = {funct3,1'b0};
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 0;       //Register file WD3 is Result
        RegWrite = 1;  // All instructions trigger a register write
        MemWrite = 0;  // No memory write takes place at this type
        
        InstructionType = 0; // Regular immediate type for ImmExt
        PCSrc = 0;     // No jumps taken, should go with regular PC+4
        ImmSrc = 3'b111;    // Sign extend with 12-bits, used with these immediate instructions
        ResultSrc = 0; // Takes the data from ALUResult
        shamtMuxSelect = 1; //Immediate for shifter shamt in
         if (funct3 == 3'b101 | funct3 == 3'b001) begin //Is a shift instruction
            SrcB_0Select = 1;
				ALUSrc = 0;
        end
        else begin
            //Set less than is already implemented in ALU with ALUControl and SrcB_0Select=0.
            SrcB_0Select = 0;
				ALUSrc = 1;    // Takes data from ExtImm 
        end
    end

    //Specifically for XORID
    7'b0001011: begin  
        InstructionType = 0; // I-type, but not used
        ALUControl = 4'b0111; // XORID here
        WD3Sel = 0;       //Register file WD3 is Result
        ALUSrc_A = 0;     //SrcA = RD1;
        RegWrite = 1;  // All instructions trigger a register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 0;    // Takes data from RD2, not extended Immediate 
        PCSrc = 0;     // No jumps taken, should go with regular PC+4
        ImmSrc = 0;    // Should not matter, to avoid latches
        ResultSrc = 0; // Takes the data from ALUResult
        shamtMuxSelect = 0;  //Register for shifter shamt in
        if (funct3 == 3'b101 | funct3 == 3'b001) begin //Is a shift instruction
            SrcB_0Select = 1;
        end
        else begin
            //Set less than is already implemented in ALU with ALUControl and SrcB_0Select=0.
            SrcB_0Select = 0;
        end

    end

    // Other I-Type Operations: LW, LH, LHU, LB, LBU  //UNSIGNED İÇİN EXTENDER EKLENDİ, EXTENDER GENİŞLETİLDİ
    7'b0000011: begin 
        ALUControl = 4'b0000; // Add operation
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 0;       //Register file WD3 is Result
        RegWrite = 1;  // All instructions trigger a register write
        InstructionType = 0; // Regular immediate type for ImmExt
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 1;    // Takes data from extended Immediate 
        PCSrc = 0;     // No jumps taken, should go with regular PC+4
        ImmSrc = 3'b111;    // Sign extend with 12-bits, used with these immediate instructions
        ResultSrc = 1; // Takes the data from MemoryExtender output.
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 1; //Uses immediate all the time.
    end

    // B-Type Instructions: BEQ, BNE, BLT, BGE, BLTU, BGEU
    // BEQ => Z == 1
    // BNE => Z == 0
    // BLT/U => N == 1
    // BGE/U => N == 0
    7'b1100011: begin 
        InstructionType = 3'b010; // B encoded immediate for ImmExt
        ALUControl = {~(funct3[2] & funct3[1]), ~(funct3[2] & funct3[1]), ~(funct3[2] & funct3[1]), 1'b1}; // SUB operation to get Zero flag nand, Gives SUB for unsigned and Signed_SUB for others
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 0;       //Register file WD3 is Result
        RegWrite = 0;  // No register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 0;    // Takes data from RD2
        ImmSrc = 3'b110;    // Branch and jump, multiples of 4
        ResultSrc = 0; //Does not matter
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 0; // ALUSrc is 0, does not matter here
        if (funct3[2] == 0) begin //BEQ or BNE
            PCSrc = {1'b0,(Zero == ~(funct3[0]))};
        end
        else if (funct3[1] == 1'b1) begin // BLTU or BGEU
            PCSrc = {1'b0,(Carry == (funct3[0]))};
        end
        else begin  //BLT or BGE
            PCSrc = {1'b0,(Negative == ~(funct3[0]))};
        end
    end

    // S-Type Instructions: SW, SH, SB
    7'b0100011: begin 
        InstructionType = 3'b001; // S encoded immediate for ImmExt
        ALUControl = 4'b0000;     // Add operation
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 0;       //Register file WD3 is Result
        RegWrite = 0;  // No register write
        MemWrite = 1;  // Memory write takes place 
        ALUSrc = 1;  //Takes data from immediate
        ImmSrc = 3'b111; // Sign extend with 12-bits, used with these immediate instructions
        ResultSrc = 1;
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 0;   //RD2 into SrcB
        PCSrc = 0;  //Regular PC+4
    end

    // U-Type Instructions: LUI
    7'b0110111: begin
        InstructionType = 3'b011; // U encoded immediate for ImmExt
        ImmSrc = 3'b011;          // Upper immediate
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 0;       //Register file WD3 is Result
        ALUControl = 4'b0101;     // Move operation
        RegWrite = 1;  // No register write
        MemWrite = 0;  // Memory write takes place 
        ALUSrc = 1;  //Takes data from immediate
        ResultSrc = 0;
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 0;   //RD2 into SrcB does not matter
        PCSrc = 0;  //Regular PC+4
    end

    // U-Type Instructions: AUIPC
    7'b0010111: begin
        InstructionType = 3'b011; // U encoded immediate for ImmExt,
        ImmSrc = 3'b011;          // Upper immediate
        ALUSrc_A = 1;     //SrcA = PC;
        WD3Sel = 0;       //Register file WD3 is Result
        ALUControl = 4'b0000;     // ADD operation
        RegWrite = 1;  // No register write
        MemWrite = 0;  // Memory write takes place 
        ALUSrc = 1;  //Takes data from immediate
        ResultSrc = 0;
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 0;   //RD2 into SrcB does not matter
        PCSrc = 0;  //Regular PC+4
    end

    // J-Type Instructions: JAL,   J-type encoding
    7'b1101111: begin
        InstructionType = 3'b100; // J encoded immediate for ImmExt
        ALUControl = {~(funct3[2] & funct3[1]), ~(funct3[2] & funct3[1]), ~(funct3[2] & funct3[1]), 1'b1}; // SUB operation to get Zero flag nand, Gives SUB for unsigned and Signed_SUB for others
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 1;       //Register file WD3 is PCPlus4
        RegWrite = 1;  // Register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 0;    // Takes data from RD2
        ImmSrc = 3'b110;    // 
        ResultSrc = 0; //Does not matter since WD3 mux governs
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 1; // ALUSrc is 0, does not matter here
        PCSrc = 1;
    end

    // J-Type Instructions: JALR,   
    7'b1100111: begin
        InstructionType = 3'b000; // J encoded immediate for ImmExt
        ALUControl = 4'b0000; //ADD operation
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 1;       //Register file WD3 is PC+4
        RegWrite = 1;  // Register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 1;    // Takes data from RD2
        ImmSrc = 3'b111;    // Sign extended
        ResultSrc = 0; //Does not matter since WD3 mux governs
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 1; // ALUSrc is 0, does not matter here
        PCSrc = 2'b10;
    end
	 default: begin
		  InstructionType = 3'b000; // J encoded immediate for ImmExt
        ALUControl = 4'b1001; //ADD operation
        ALUSrc_A = 0;     //SrcA = RD1;
        WD3Sel = 1;       //Register file WD3 is PC+4
        RegWrite = 1;  // Register write
        MemWrite = 0;  // No memory write takes place at this type
        ALUSrc = 1;    // Takes data from RD2
        ImmSrc = 3'b111;    // Sign extended
        ResultSrc = 0; //Does not matter since WD3 mux governs
        shamtMuxSelect = 1;  // Is not needed here, does not matter
        SrcB_0Select = 1; // ALUSrc is 0, does not matter here
        PCSrc = 2;
		  end

endcase
end

endmodule