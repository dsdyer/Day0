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
      if re.match("//", line) or not re.match(".", line):
        pass # current line is blank or whitespace
      else:
        self.commands.append(line.replace("\n", "").split(' '))
    self.commands = iter(self.commands)
    self.current = ''
  def showLines(self):
    for line in self.file:
      print(line)
    
  def advance(self):
    self.current = self.commands.__next__()
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
  def __init__(self, arg):
    self.arg = arg
  def setFileName(self, file_name):
    pass
  def writeArithmetic(self, command):
    pass
  def writePushPop(self, command):
    pass
    

if __name__ == "__main__":
  target = sys.argv[1]

  if re.search("\.vm$", str(target)):     # if the argument was one .vm file, parse it
    file = sys.argv[1]
    p = Parser(file)
  else:                                   # if the argument is not a .vm file, try to
    files = glob.glob(target + '/*.vm')   # treat it as a directory containing .vm files
    if len(files) >= 1:
      for x in files:
        p = Parser(x)
    else:                                 # if that fails tell them
      raise Exception('Bad input. You fix.')

  while True:
    try:
      p.advance()
      print(p.arg2())
    except(StopIteration):
      print('all done')
      break
