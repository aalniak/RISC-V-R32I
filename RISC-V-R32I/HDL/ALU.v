module ALU #(parameter WIDTH=8)
    (
	  input [3:0]            control,
	  input [WIDTH-1:0]      DATA_A,
	  input [WIDTH-1:0]      DATA_B,
      output reg [WIDTH-1:0] OUT,
	  output reg             CO,
	  output reg             OVF,
	  output                 N, Z
    );
localparam //control = {funct3&funct7_6}
		  AND = 4'b1110,
		  EXOR = 4'b1000,
		  SUB = 4'b0001,
		  Signed_SUB = 4'b1111,
		  ADD = 4'b0000,
		  ORR = 4'b1100,
		  SLL = 4'b0010,
		  SRL = 4'b1010,
		  SRA = 4'b1011,
		  SLT = 4'b0100,
		  SLTU = 4'b0110,
		  MOV = 4'b0101,
		  ADD_0 = 4'b1001,
		  XORID = 4'b0111;
		  

// Assign the zero and negative flasg here since it is very simple
assign N = OUT[WIDTH-1];
assign Z = ~(|OUT);
reg [31:0] Intermediate_OUT = 0; 
always@(*) begin
	CO = 0;
	OVF = 0;
	Intermediate_OUT =0;
	case(control)
		XORID:begin
			OUT = DATA_A ^ (32'd2442390 ^ 32'd2442986);
		end
		MOV:begin
			OUT = DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		ADD_0:begin
			{CO,OUT} = (DATA_A + DATA_B);
			OUT = {Intermediate_OUT[30:0],1'b0};
			OVF = (DATA_A[WIDTH-1] & DATA_B[WIDTH-1] & ~OUT[WIDTH-1]) | (~DATA_A[WIDTH-1] & ~DATA_B[WIDTH-1] & OUT[WIDTH-1]);
		end
		AND:begin
			OUT = DATA_A & DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		EXOR:begin
			OUT = DATA_A ^ DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		SUB:begin
			{CO,OUT} =  DATA_A +  $unsigned(~DATA_B) +  1'b1;
			OVF = (DATA_A[WIDTH-1] & ~DATA_B[WIDTH-1] & ~OUT[WIDTH-1]) | (~DATA_A[WIDTH-1] & DATA_B[WIDTH-1] & OUT[WIDTH-1]);
		end
		Signed_SUB:begin
			{CO, OUT} = $signed(DATA_A) - $signed(DATA_B);
			OVF = 0; //See if needs implementation, I suspect not
		end
		ADD:begin
			{CO,OUT} = DATA_A + DATA_B;
			OVF = (DATA_A[WIDTH-1] & DATA_B[WIDTH-1] & ~OUT[WIDTH-1]) | (~DATA_A[WIDTH-1] & ~DATA_B[WIDTH-1] & OUT[WIDTH-1]);
		end
		ORR:begin
			OUT = DATA_A | DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		SLL:begin
			OUT = DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		SRL:begin
			OUT = DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		SRA:begin
			OUT = DATA_B;
			CO = 1'b0;
			OVF = 1'b0;
		end
		SLT:begin
			OUT = ($signed(DATA_A) < $signed(DATA_B)) ? 1 : 0;
			CO = 1'b0; //CARRY OUT OVF FALAN Kontrol edilebilir LAZIM OLMUYO SANIRIM RISCVDA AMA
			OVF = 1'b0;
		end
		SLTU:begin
			OUT = (DATA_A < DATA_B) ? 1 : 0;
			CO = 1'b0;
			OVF = 1'b0;
		end
		default:begin
		OUT = ($signed(DATA_A) < $signed(DATA_B)) ? 1 : 0;
			CO = 1'b0; //CARRY OUT OVF FALAN Kontrol edilebilir LAZIM OLMUYO SANIRIM RISCVDA AMA
			OVF = 1'b0;
		end
	endcase
end
	 
endmodule	 