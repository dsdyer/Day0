@ARG
D=M
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
@0
D=A
@0
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@0
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
@0
D=A
@1
AD=D+A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@1
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
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
@ARG
D=M
@0
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
(FibonacciSeries$MAIN_LOOP_START)
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
@SP
AM=M-1
D=M
@FibonacciSeries$COMPUTE_ELEMENT
D;JNE
@FibonacciSeries$END_PROGRAM
0;JMP
(FibonacciSeries$COMPUTE_ELEMENT)
@THAT
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@1
AD=D+A
D=M
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
M=D+M
@SP
M=M+1
@THAT
D=M
@2
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
@3
D=A
@1
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
M=D+M
@SP
M=M+1
@3
D=A
@1
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
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
@ARG
D=M
@0
AD=D+A
@R14
M=D
@SP
AM=M-1
D=M
@R14
A=M
M=D
@FibonacciSeries$MAIN_LOOP_START
0;JMP
(FibonacciSeries$END_PROGRAM)
