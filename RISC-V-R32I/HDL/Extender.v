module Extender #(parameter WIDTH=32) (
    output reg [31:0]Extended_data,
    input [WIDTH-1:0]DATA,
    input [2:0] select,
    input [2:0] instruction_type
);
reg [31:0] IntermediateData;
always @(*) begin
    case (instruction_type)
        3'b000 : IntermediateData = {20'd0,DATA[31:20]}; //I Regular Immediate with 12-bits of 0 and 12-bits of lower data bits
        3'b001 : IntermediateData = {20'd0,DATA[31:25],DATA[11:7]};  //S Store type immediate with 12-bits of 0 and 
        3'b010 : IntermediateData = {20'd0,DATA[31],DATA[7],DATA[30:25],DATA[11:8]}; //B type
        3'b011 : IntermediateData = {4'd0,DATA[31:12]}; //U type
        3'b100 : IntermediateData = {12'd0,DATA[31],DATA[19:12],DATA[20],DATA[30:21]}; //J type
		  3'b101 : IntermediateData = DATA;
		  default: IntermediateData = 0;
    endcase
    case (select)
        //2'b00: Extended_data = {24'd0, DATA[7:0]};
        //2'b01: Extended_data = {20'd0, DATA[11:0]};

        //Instructions in this scope is used for Memory Extender
        3'b100: Extended_data = {24'd0, IntermediateData[7:0]}; //LBU
        3'b000: Extended_data = {{24{IntermediateData[7]}}, DATA[7:0]}; //LB
        3'b101: Extended_data = {16'd0, IntermediateData[15:0]}; //LHU
        3'b001: Extended_data = {{16{IntermediateData[15]}}, IntermediateData[15:0]}; //LH
        3'b010: Extended_data = IntermediateData; //LW
        3'b011: Extended_data = {IntermediateData[19:0],12'd0};
        //Instructions in this scope is used for Immediate Extender
        3'b110: Extended_data = {{12{IntermediateData[19]}}, IntermediateData[19:0], 1'b0}; //for jumps
        3'b111: Extended_data = {{20{IntermediateData[11]}}, IntermediateData[11:0]}; //12-bit sign extended
        default: Extended_data = 32'd0;
    endcase
end
    
endmodule
