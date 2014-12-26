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
    self.current = self.commands.__next__()
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
  
  def writePushPop(self, c, pointer=False):
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
    pointer_type = 'A' if pointer else segments[segment][1]

    #find the requested address and store it in D:
    if segment == "static":
      find_address = [
        "@" + self.file_name + "." + str(index),
        "D=M"
      ]
    else:
      find_address = [
        "@" + segments[segment][0],
        "D=" + pointer_type,
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
  def writeInit(self):
    assembly = [
      "@256",
      "D=A",
      "@SP",
      "M=D"
    ]
    assembly.extend(self.writeCall(['call', 'Sys.init', '0']))
    return assembly
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
    segments = ["local", "argument", "this", "that"]
    assembly = [
      '@' + return_address,
      'D=A',
      '@SP',
      'A=M',
      'M=D',
      '@SP',
      'M=M+1'
    ]
    for a in segments:
      assembly.extend(self.writePushPop(['push', a, '0'], True))
    assembly.extend([
        "@SP",
        "D=M",
        "@" + str(int(args)),
        "D=D-A", # D = SP - number of args
        "@5",
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
    assembly = ['//start return']
    assembly.extend(self.writePushPop(['push', 'local', '0'], True)) # push the memory address stored at LCL
    assembly.extend(self.writePushPop(['pop', 'temp', '0'])) # store local in a temporary variable
    assembly.extend([
    	'//LCL is stored in temp[0], which is R5',
    	'@LCL',
    	'D=M',
    	'@5',
    	'A=D-A //LCL-5',
      'D=M',
      '@R6',
      'M=D // Return address is stored in R6'
    ])
    assembly.extend(self.writePushPop(['pop', 'argument', '0']))
    assembly.extend([
      '@ARG',
      'D=M',
      '@1',
      'D=D+A',
      '@SP',
      'M=D',
      '@R5',
      'D=M',
      '@1',
      'A=D-A',
      'D=M',
      '@THAT',
      'M=D',
      '@R5',
      'D=M',
      '@2',
      'A=D-A',
      'D=M',
      '@THIS',
      'M=D',
      '@R5',
      'D=M',
      '@3',
      'A=D-A',
      'D=M',
      '@ARG',
      'M=D',
      '@R5',
      'D=M',
      '@4',
      'A=D-A',
      'D=M',
      '@LCL',
      'M=D',
      '@R6',
      'A=M',
      '0;JMP'
      ])
    return assembly

  def writeFunction(self, c):
    assembly = ["(" + self.working_parser.arg1() + ")"]
    for n in range(int(c[2])):
      assembly.extend(self.writePushPop(["push", "constant", "0"]))
    print(assembly)
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
  # if some bullshit:
  #   x.output_file.write("\n".join(x.writeArithmetic(c)) + "\n")

  # parsers.insert(0, parsers.pop(parsers.index('Sys')))

  for a in parsers:
    if a.name == "Sys":
      parsers.insert(0, parsers.pop(parsers.index(a)))

  for a in parsers:
    if a.name == 'Sys':
      print('sysing')
      x.setParser(a)
      x.output_file.write("\n".join(x.writeInit()) + "\n")
    else:
      print('maining')
      x.setParser(a)
    while True:
      try: 
        c = x.working_parser.advance()
        t = x.working_parser.commandType()
        if t == "C_ARITHMETIC":
          x.output_file.write("\n".join(x.writeArithmetic(c)) + "\n")
        elif t in ("C_PUSH", "C_POP"):
          x.output_file.write("\n".join(x.writePushPop(c)) + "\n")
        elif t == "C_LABEL":
          x.output_file.write("\n".join(x.writeLabel(c)) + "\n")
        elif t == "C_GOTO":
          x.output_file.write("\n".join(x.writeGoto(c)) + "\n")
        elif t == "C_IF":
          x.output_file.write("\n".join(x.writeIf(c)) + "\n")
        elif t == "C_CALL":
          x.output_file.write("\n".join(x.writeCall(c)) + "\n")
        elif t == "C_RETURN":
          x.output_file.write("\n".join(x.writeReturn()) + "\n")
        elif t == "C_FUNCTION":
          x.output_file.write("\n".join(x.writeFunction(c)) + "\n")
          print(c)
      except(StopIteration):
        break
