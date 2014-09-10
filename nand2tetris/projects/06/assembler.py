# Assembles .asm files into machine code

import re

class Parser:
    def __init__(self, input_tuple):
        # openInputFile
            # returns input_array, each item of which is a line from the input file
        self.commands = len(input_tuple)
        self.currentPosition = 0
        self.currentCommand = input_tuple[0]
    def advance(self):
        if self.hasMoreCommands():
            self.currentPosition += 1
            self.currentCommand = input_tuple[self.currentPosition]
    def showCurrent(self):
        print(self.currentCommand)
    def hasMoreCommands(self):
        if self.currentPosition == self.commands - 1:
            return False
        return True
    def commandType(self):
        if re.match("@", self.currentCommand):
            return "A_COMMAND"
        elif re.search("=", self.currentCommand):
            return "C_COMMAND"
        elif re.match("\(", self.currentCommand):
            return "L_COMMAND"
        else:
            raise Exception("Bad command: Check line " + str(self.currentPosition -1) + " of the input file")
        

input_tuple = ("dest=comp;jump", "@3", "(0010011101101100)", "junk")
x = Parser(input_tuple)
x.advance()
x.advance()
x.advance()

x.showCurrent()
print(x.commandType())


