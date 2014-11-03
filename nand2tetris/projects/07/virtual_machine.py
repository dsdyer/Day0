import sys
import re
import glob

class Parser(object):
  """prepares inputs for translation into assembly code"""
  
  def __init__(self, arg):
    self.arg = arg
    self.file = open(self.arg, "r") # open the file
    self.commands = []

    for line in self.file:
      if re.match("//", line) or not re.match("[^\r\n]", line):
        pass # current line is blank or whitespace
      else:
        self.commands.append(line.replace("\r", "").replace("\n", "").split(' '))
    self.commands = iter(self.commands)
    self.current = ''
  
  def showLines(self):
    for line in self.file:
      print(line)
    
  def advance(self):
    self.current = self.commands.next()
    return self.current
    
  def commandType(self):
    types = {
      'add' : 'C_ARITHMETIC',
      'sub' : 'C_ARITHMETIC',
      'neg' : 'C_ARITHMETIC',
      'eq' : 'C_ARITHMETIC',
      'gt' : 'C_ARITHMETIC',
      'lt' : 'C_ARITHMETIC',
      'and' : 'C_ARITHMETIC',
      'or' : 'C_ARITHMETIC',
      'not' : 'C_ARITHMETIC',
      'push' : 'C_PUSH',
      'pop' : 'C_POP',
      'label' : 'C_LABEL',
      'goto' : 'C_GOTO',
      'if-goto' : 'C_IF',
      'function' : 'C_FUNCTION',
      'return' : 'C_RETURN',
      'call' : 'C_CALL',
    }
    return types[self.current[0]]
        
  def arg1(self):
    if self.commandType() == 'C_ARITHMETIC':
      return self.current[0]
    else:
      return self.current[1]

  def arg2(self):
    if self.commandType() == 'C_PUSH':
      return self.current[2]

class CodeWriter(object):
  """docstring for CodeWriter"""
  
  def __init__(self):
    self.output_file = open("vm_output.asm", "w+")
    self.working_parser = {}
    self.labelID = 0;

  def setFileName(self, parser):
    self.working_parser = parser

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
        "TRUE"  : self.uniqueLabel('TRUE'), 
        "FALSE" : self.uniqueLabel('FALSE'), 
        "END"   : self.uniqueLabel('END')
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
        "TRUE"  : self.uniqueLabel('TRUE'), 
        "FALSE" : self.uniqueLabel('FALSE'), 
        "END"   : self.uniqueLabel('END')
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
        "TRUE"  : self.uniqueLabel('TRUE'), 
        "FALSE" : self.uniqueLabel('FALSE'), 
        "END"   : self.uniqueLabel('END')
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
      raise(Exception('Something isn\'t right!'))
    return assembly
  
  def writePushPop(self, command):
    if command[0] == "push":
      source = command[1]
      pushables = {
        "constant" : command[2]
      }
      assembly = [
        "@" + pushables[source],
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
      ]
    return assembly
    

if __name__ == "__main__":
  target = sys.argv[1]
  parsers = []

  if re.search("\.vm$", str(target)):     # if the argument was one .vm file, parse it
    file = sys.argv[1]
    p = Parser(file)
    parsers.append(p)
  else:                                   # if the argument is not a .vm file, try to
    files = glob.glob(target + '/*.vm')   # treat it as a directory containing .vm files
    if len(files) >= 1:
      for x in files:
        p = Parser(x)
        parsers.append(p)
    else:                                 # if that fails tell them
      raise Exception('Bad input. You fix.')

  x = CodeWriter()

  for a in parsers:
    x.setFileName(a)
    while True:
      try: 
        c = x.working_parser.advance()
        if x.working_parser.commandType() == 'C_ARITHMETIC':
          x.output_file.write("\n".join(x.writeArithmetic(c)) + "\n")

        if x.working_parser.commandType() == 'C_PUSH':
          x.output_file.write("\n".join(x.writePushPop(c)) + "\n")

      except(StopIteration):
        break