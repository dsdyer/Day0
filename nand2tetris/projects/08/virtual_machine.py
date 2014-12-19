import sys
import re
import glob

class Parser(object):
  """prepares inputs for translation into assembly code"""
  
  def __init__(self, arg):
    self.arg = arg
    self.file = open(self.arg, "r") # open the file
    self.name = re.findall("(\w+)\.vm$", self.file.name)[0]
    self.commands = []

    for line in self.file:
      if re.match("//", line) or not re.match("[^\r\n]", line):
        pass # current line is blank or whitespace
      else:
        self.commands.append(line.replace("\r", "").replace("\n", "").split(" "))
    self.commands = iter(self.commands)
    self.current = ""
  
  def showLines(self):
    for line in self.file:
      print(line)
    
  def advance(self):
    self.current = self.commands.next()
    return self.current
    
  def commandType(self):
    types = {
      "add"      : "C_ARITHMETIC",
      "sub"      : "C_ARITHMETIC",
      "neg"      : "C_ARITHMETIC",
      "eq"       : "C_ARITHMETIC",
      "gt"       : "C_ARITHMETIC",
      "lt"       : "C_ARITHMETIC",
      "and"      : "C_ARITHMETIC",
      "or"       : "C_ARITHMETIC",
      "not"      : "C_ARITHMETIC",
      "push"     : "C_PUSH",
      "pop"      : "C_POP",
      "label"    : "C_LABEL",
      "goto"     : "C_GOTO",
      "if-goto"  : "C_IF",
      "function" : "C_FUNCTION",
      "return"   : "C_RETURN",
      "call"     : "C_CALL",
    }
    return types[self.current[0]]
        
  def arg1(self):
    if self.commandType() == "C_ARITHMETIC":
      return self.current[0]
    else:
      return self.current[1]

  def arg2(self):
    if self.commandType() == "C_PUSH":
      return self.current[2]

class CodeWriter(object):
  """docstring for CodeWriter"""
  
  def __init__(self):
    self.output_file = open("vm_output.asm", "w+")
    self.working_parser = {}
    self.labelID = 0

  def setParser(self, parser):
    self.working_parser = parser
    self.file_name = self.working_parser.name

  def setFileName(self, name):
    self.file_name = name

  def uniqueLabel(self, label):
    unique_label = label + str(self.labelID)
    self.labelID += 1
    return unique_label

  def writeArithmetic(self, command):
    if command[0] == "add":
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "M=D+M",
        "@SP",
        "M=M+1"
      ]
    elif command[0] == "sub":
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "M=M-D",
        "@SP",
        "M=M+1"
      ]
    elif command[0] == "neg":
      assembly = [
        "@SP",
        "AM=M-1",
        "M=-M",
        "@SP",
        "M=M+1"
      ]
    elif command[0] == "eq":
      labels = { 
        "TRUE"  : self.uniqueLabel("TRUE"), 
        "FALSE" : self.uniqueLabel("FALSE"), 
        "END"   : self.uniqueLabel("END")
      }
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "D=M-D",
        "@" + labels["TRUE"],
        "D;JEQ",
        "@" + labels["FALSE"],
        "D;JNE",
        "(" + labels["TRUE"] + ")",
        "@SP",
        "A=M",
        "M=-1",
        "@SP",
        "M=M+1",
        "@" + labels["END"],
        "0;JMP",
        "(" + labels["FALSE"] + ")",
        "@SP",
        "A=M",
        "M=0",
        "@SP",
        "M=M+1",
        "(" + labels["END"] + ")",
      ]
    elif command[0] == "gt":
      labels = { 
        "TRUE"  : self.uniqueLabel("TRUE"), 
        "FALSE" : self.uniqueLabel("FALSE"), 
        "END"   : self.uniqueLabel("END")
      }
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "D=M-D",
        "@" + labels["TRUE"],
        "D;JGT",
        "@" + labels["FALSE"],
        "D;JLE",
        "(" + labels["TRUE"] + ")",
        "@SP",
        "A=M",
        "M=-1",
        "@SP",
        "M=M+1",
        "@" + labels["END"],
        "0;JMP",
        "(" + labels["FALSE"] + ")",
        "@SP",
        "A=M",
        "M=0",
        "@SP",
        "M=M+1",
        "(" + labels["END"] + ")",
      ]
    elif command[0] == "lt":
      labels = { 
        "TRUE"  : self.uniqueLabel("TRUE"), 
        "FALSE" : self.uniqueLabel("FALSE"), 
        "END"   : self.uniqueLabel("END")
      }
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "D=M-D",
        "@" + labels["TRUE"],
        "D;JLT",
        "@" + labels["FALSE"],
        "D;JGE",
        "(" + labels["TRUE"] + ")",
        "@SP",
        "A=M",
        "M=-1",
        "@SP",
        "M=M+1",
        "@" + labels["END"],
        "0;JMP",
        "(" + labels["FALSE"] + ")",
        "@SP",
        "A=M",
        "M=0",
        "@SP",
        "M=M+1",
        "(" + labels["END"] + ")",
      ]
    elif command[0] == "and":
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "M=D&M",
        "@SP",
        "M=M+1"
      ]
    elif command[0] == "or":
      assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@SP",
        "AM=M-1",
        "M=D|M",
        "@SP",
        "M=M+1"
      ]
    elif command[0] == "not":
      assembly = [
        "@SP",
        "AM=M-1",
        "M=!M",
        "@SP",
        "M=M+1"
      ]
    else:
      raise(Exception("Something isn\"t right!"))
    return assembly
  
  def writePushPop(self, c):
    filename = re.findall("(\w+)\.vm$", self.working_parser.arg)[0]
    command = c[0]
    segment = c[1]
    index = c[2]
    segments = {
      "constant" : ["0", "A"],
      "pointer"  : ["3", "A"],
      "temp"     : ["5", "A"],
      "local"    : ["LCL", "M"],
      "this"     : ["THIS", "M"],
      "that"     : ["THAT", "M"],
      "argument" : ["ARG", "M"],
    }
    #find the requested address and store it in D:
    if segment == "static":
      find_address = [
        "@" + self.file_name + "." + str(index),
        "D=M"
      ]
    else:
      find_address = [
        "@" + segments[segment][0],
        "D=" + segments[segment][1],
        "@" + str(index),
        "AD=D+A"
      ]
    if command == "push":
      if segment not in ("constant", "static"):
        find_address = find_address + ["D=M"]
      assembly = find_address + [
        #put D on top of the stack:
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
      ]

    elif command == "pop":
      assembly = find_address + [
        "@R14", # target memory address stored at R14
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M", # top value of the stack stored at D
        "@R14",
        "A=M", 
        "M=D"
      ]
    return assembly
  def writeInit(self, c):
    assembly = [
      "@256",
      "D=A",
      "@SP",
      "M=D"
      # Stack pointer is now set to 256, you need to call Sys.init,
      # Whatever that means
    ]
  def writeLabel(self, c):
    assembly = ["(" + self.file_name + "$" + self.working_parser.arg1() + ")"]
    return assembly
  def writeGoto(self, c):
    label = self.file_name + "$" + self.working_parser.arg1()
    assembly = [
      "@" + label,
      "0;JMP"
    ]
    return assembly
  def writeIf(self, c):
    label = self.file_name + "$" + self.working_parser.arg1()
    assembly = [
      "@SP",
      "AM=M-1",
      "D=M",
      "@" + label,
      "D;JNE"
    ]
    return assembly
  def writeCall(self, c):
    return_address = self.uniqueLabel("return_address")
    args = c[2]
    segments = [return_address, "LCL", "ARG", "THIS", "THAT"]
    assembly = []
    for a in segments:
      assembly.extend([
        "@" + a,
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
        ])
    assembly.extend([
        "@SP",
        "D=M",
        "@" + str(int(args) - 5),
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        "@" + c[1],
        "0;JMP",
        "(" + return_address + ")"
      ])
    return assembly

  def writeReturn(self):
    assembly = [
      "@LCL",
      "D=M",
      "@5",
      "M=D", #temp 0 holds LCL (call this FRAME)
      "@5",
      "D=D-A",
      "@6",
      "M=D", #temp 1 holds return_address (call this RET)
      "@SP",
      "AM=M-1",
      "D=M",
      "@ARG",
      "M=D",
      "D=A+1",
      "@SP",
      "M=D",
      "@5", #get FRAME
      "MD=M-1",
      "@THAT",
      "M=D",
      "@5",
      "MD=M-1",
      "@THIS",
      "M=D",
      "@5", 
      "MD=M-1",
      "@ARG",
      "M=D",
      "@5",
      "MD=M-1",
      "@LCL",
      "M=D",
      "@6",
      "A=M",
      "0;JMP"
    ]
    return assembly
  def writeFunction(self, c):
    self.setFileName(self.working_parser.arg1())
    assembly = ["(" + self.file_name + ")"]
    for n in range(int(c[2])):
      assembly.extend(self.writePushPop(["push", "constant", "0"]))
    return assembly
    
if __name__ == "__main__":
  target = sys.argv[1]
  parsers = []

  if re.search("\.vm$", str(target)):     # if the argument was one .vm file, parse it
    p = Parser(target)
    parsers.append(p)
  else:                                   # if the argument is not a .vm file, try to
    files = glob.glob(target + "/*.vm")   # treat it as a directory containing .vm files
    if len(files) >= 1:
      for x in files:
        p = Parser(x)
        parsers.append(p)
    else:                                 # if that fails tell them
      raise Exception("Input is not a VM file or directory. Getting kinda tired of your shit.")

  x = CodeWriter()

  for a in parsers:
    x.setParser(a)
    while True:
      try: 
        c = x.working_parser.advance()
        t = x.working_parser.commandType()
        if t == "C_ARITHMETIC":
          x.output_file.write("\n".join(x.writeArithmetic(c)) + "\n")
        elif t in ("C_PUSH", "C_POP"):
          x.output_file.write("\n".join(x.writePushPop(c)) + "\n")
        if t == "C_LABEL":
          x.output_file.write("\n".join(x.writeLabel(c)) + "\n")
        if t == "C_GOTO":
          x.output_file.write("\n".join(x.writeGoto(c)) + "\n")
        if t == "C_IF":
          x.output_file.write("\n".join(x.writeIf(c)) + "\n")
        if t == "C_CALL":
          x.output_file.write("\n".join(x.writeCall(c)) + "\n")
        if t == "C_RETURN":
          x.output_file.write("\n".join(x.writeReturn()) + "\n")
        if t == "C_FUNCTION":
          x.output_file.write("\n".join(x.writeFunction(c)) + "\n")
      except(StopIteration):
        break
