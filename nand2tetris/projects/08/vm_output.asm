Main.fibonacci
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@2
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE0
D;JLT
@FALSE1
D;JGE
(TRUE0)
@SP
A=M
M=-1
@SP
M=M+1
@END2
0;JMP
(FALSE1)
@SP
A=M
M=0
@SP
M=M+1
(END2)
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
@Main.fibonacci$IF_FALSE
0;JMP
(Main.fibonacci$IF_TRUE)
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
return
(Main.fibonacci$IF_FALSE)
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@2
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
call: 
@return_address3
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@-4
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address3)
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@1
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
call: 
@return_address4
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@-4
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address4)
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
return
Sys.init
@0
D=A
@4
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
call: 
@return_address5
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@-4
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address5)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
