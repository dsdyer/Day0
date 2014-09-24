import sys
import re
import glob

class Parser(object):
  """prepares inputs for translation into assembly code"""
  def __init__(self, arg):
    self.arg = arg
    self.file = open(self.arg, "r")
  def showLines(self):
    for line in self.file:
      print(line)

if __name__ == "__main__":
  target = sys.argv[1]

  if re.search("\.vm$", str(target)):     # if the argument was one .vm file, parse it
    file = sys.argv[1]
    p = Parser(file)
    p.showLines()
  else:                                   # if the argument is not a .vm file, try to
    files = glob.glob(target + '/*.vm')   # treat it as a directory containing .vm files
    if len(files) >= 1:
      for x in files:
        p = Parser(x)
        p.showLines()
    else:                                 # if that fails tell them
      raise Exception('Bad input. You fix.')
