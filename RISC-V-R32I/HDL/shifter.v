module shifter #(
     parameter WIDTH=32)
    (
	  input [1:0]  				 	control,
	  input [4:0] 				 	shamt,
	  input signed [WIDTH-1:0]	 	DATA,
	  output reg signed [WIDTH-1:0] OUT
    );
	 
localparam LSL=2'b00,
		  LSR=2'b01,
		  RR=2'b10,
		  ASR=2'b11;	
	 
always@(*) begin
	case(control)
	LSL: OUT = DATA << shamt;
	LSR: OUT = DATA >> shamt;
	ASR: OUT = DATA >>> shamt;
	RR: OUT = {DATA, DATA} >> shamt;
	endcase
end
	 
endmodule	 