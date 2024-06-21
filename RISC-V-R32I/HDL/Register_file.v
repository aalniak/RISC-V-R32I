module Register_file #(parameter WIDTH=32)
    (
	  input              clk, write_enable, reset,
	  input [4:0]        Source_select_0, Source_select_1, Debug_Source_select, Destination_select,
	  input	[WIDTH-1:0]  DATA, 
	  output [WIDTH-1:0] out_0, out_1, Debug_out                                                    
    );

wire [WIDTH-1:0] Reg_Out [31:0];
wire [31:0] Reg_enable;


genvar i;
Register_rsten_neg #(WIDTH) Reg0 (.clk(clk),.reset(reset),.we(1'b0),.DATA(DATA),.OUT(Reg_Out[0]));
generate
    for (i = 1 ; i < 32 ; i = i + 1) begin : registers
        Register_rsten_neg #(WIDTH) Reg (.clk(clk),.reset(reset),.we(Reg_enable[i]& write_enable),.DATA(DATA),.OUT(Reg_Out[i]));
    end
endgenerate

Decoder_5to32 dec (.IN(Destination_select),.OUT(Reg_enable));

Mux_16to1 #(.WIDTH(32)) mux_0 (.select(Source_select_0),
	.input_0 (Reg_Out[0]),
	.input_1 (Reg_Out[1]),
	.input_2 (Reg_Out[2]),
	.input_3 (Reg_Out[3]),
	.input_4 (Reg_Out[4]),
	.input_5 (Reg_Out[5]),
	.input_6 (Reg_Out[6]),
	.input_7 (Reg_Out[7]),
	.input_8 (Reg_Out[8]),
	.input_9 (Reg_Out[9]),
	.input_10(Reg_Out[10]),
	.input_11(Reg_Out[11]),
	.input_12(Reg_Out[12]),
	.input_13(Reg_Out[13]),
	.input_14(Reg_Out[14]),
	.input_15(Reg_Out[15]),
	.input_16(Reg_Out[16]),
	.input_17(Reg_Out[17]),
	.input_18(Reg_Out[18]),
	.input_19(Reg_Out[19]),
	.input_20(Reg_Out[20]),
	.input_21(Reg_Out[21]),
	.input_22(Reg_Out[22]),
	.input_23(Reg_Out[23]),
	.input_24(Reg_Out[24]),
	.input_25(Reg_Out[25]),
	.input_26(Reg_Out[26]),
	.input_27(Reg_Out[27]),
	.input_28(Reg_Out[28]),
	.input_29(Reg_Out[29]),
	.input_30(Reg_Out[30]),
	.input_31(Reg_Out[31]),
	.output_value(out_0)
    );
	
Mux_16to1 #(.WIDTH(32)) mux_1 (.select(Source_select_1),
	.input_0 (Reg_Out[0]),
	.input_1 (Reg_Out[1]),
	.input_2 (Reg_Out[2]),
	.input_3 (Reg_Out[3]),
	.input_4 (Reg_Out[4]),
	.input_5 (Reg_Out[5]),
	.input_6 (Reg_Out[6]),
	.input_7 (Reg_Out[7]),
	.input_8 (Reg_Out[8]),
	.input_9 (Reg_Out[9]),
	.input_10(Reg_Out[10]),
	.input_11(Reg_Out[11]),
	.input_12(Reg_Out[12]),
	.input_13(Reg_Out[13]),
	.input_14(Reg_Out[14]),
	.input_15(Reg_Out[15]),
	.input_16(Reg_Out[16]),
	.input_17(Reg_Out[17]),
	.input_18(Reg_Out[18]),
	.input_19(Reg_Out[19]),
	.input_20(Reg_Out[20]),
	.input_21(Reg_Out[21]),
	.input_22(Reg_Out[22]),
	.input_23(Reg_Out[23]),
	.input_24(Reg_Out[24]),
	.input_25(Reg_Out[25]),
	.input_26(Reg_Out[26]),
	.input_27(Reg_Out[27]),
	.input_28(Reg_Out[28]),
	.input_29(Reg_Out[29]),
	.input_30(Reg_Out[30]),
	.input_31(Reg_Out[31]),
	.output_value(out_1)
    );
	 
Mux_16to1 #(.WIDTH(32)) mux_2 (.select(Debug_Source_select),
	.input_0 (Reg_Out[0]),
	.input_1 (Reg_Out[1]),
	.input_2 (Reg_Out[2]),
	.input_3 (Reg_Out[3]),
	.input_4 (Reg_Out[4]),
	.input_5 (Reg_Out[5]),
	.input_6 (Reg_Out[6]),
	.input_7 (Reg_Out[7]),
	.input_8 (Reg_Out[8]),
	.input_9 (Reg_Out[9]),
	.input_10(Reg_Out[10]),
	.input_11(Reg_Out[11]),
	.input_12(Reg_Out[12]),
	.input_13(Reg_Out[13]),
	.input_14(Reg_Out[14]),
	.input_15(Reg_Out[15]),
	.input_16(Reg_Out[16]),
	.input_17(Reg_Out[17]),
	.input_18(Reg_Out[18]),
	.input_19(Reg_Out[19]),
	.input_20(Reg_Out[20]),
	.input_21(Reg_Out[21]),
	.input_22(Reg_Out[22]),
	.input_23(Reg_Out[23]),
	.input_24(Reg_Out[24]),
	.input_25(Reg_Out[25]),
	.input_26(Reg_Out[26]),
	.input_27(Reg_Out[27]),
	.input_28(Reg_Out[28]),
	.input_29(Reg_Out[29]),
	.input_30(Reg_Out[30]),
	.input_31(Reg_Out[31]),
	.output_value(Debug_out)
    );	 

endmodule
