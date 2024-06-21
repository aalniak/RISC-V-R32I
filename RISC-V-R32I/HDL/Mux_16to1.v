module Mux_16to1 #(parameter WIDTH=5)
    (
	  input [4:0] select,
	  input [WIDTH-1:0] input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14, input_15,
      input [WIDTH-1:0] input_16,
	  input [WIDTH-1:0] input_17,
	  input [WIDTH-1:0] input_18,
	  input [WIDTH-1:0] input_19,
	  input [WIDTH-1:0] input_20,
	  input [WIDTH-1:0] input_21,
	  input [WIDTH-1:0] input_22,
	  input [WIDTH-1:0] input_23,
	  input [WIDTH-1:0] input_24,
	  input [WIDTH-1:0] input_25,
	  input [WIDTH-1:0] input_26,
	  input [WIDTH-1:0] input_27,
	  input [WIDTH-1:0] input_28,
	  input [WIDTH-1:0] input_29,
	  input [WIDTH-1:0] input_30,
	  input [WIDTH-1:0] input_31,
	  output reg [WIDTH-1:0] output_value
    );

always@(*) begin
	case(select)
		5'b00000:output_value = input_0;
		5'b00001:output_value = input_1;
		5'b00010:output_value = input_2;
		5'b00011:output_value = input_3;
		5'b00100:output_value = input_4;
		5'b00101:output_value = input_5;
		5'b00110:output_value = input_6;
		5'b00111:output_value = input_7;
		5'b01000:output_value = input_8;
		5'b01001:output_value = input_9;
		5'b01010:output_value = input_10;
		5'b01011:output_value = input_11;
		5'b01100:output_value = input_12;
		5'b01101:output_value = input_13;
		5'b01110:output_value = input_14;
		5'b01111:output_value = input_15;
		5'b10000:output_value = input_16;
		5'b10001:output_value = input_17;
		5'b10010:output_value = input_18;
		5'b10011:output_value = input_19;
		5'b10100:output_value = input_20;
		5'b10101:output_value = input_21;
		5'b10110:output_value = input_22;
		5'b10111:output_value = input_23;
		5'b11000:output_value = input_24;
		5'b11001:output_value = input_25;
		5'b11010:output_value = input_26;
		5'b11011:output_value = input_27;
		5'b11100:output_value = input_28;
		5'b11101:output_value = input_29;
		5'b11110:output_value = input_30;
		5'b11111:output_value = input_31;
		
		default: output_value = {WIDTH{1'b0}};
	endcase
end

endmodule
