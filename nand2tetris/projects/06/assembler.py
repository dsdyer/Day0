# Assembles .asm files into machine code

import re

class Parser:
    def __init__(self, input_tuple):
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
        elif re.search("=|;", self.currentCommand):
            return "C_COMMAND"
        elif re.match("\(", self.currentCommand):
            return "L_COMMAND"
        else:
            raise Exception("Bad command: Check line " + str(self.currentPosition +1) + " of the input file")
    def dest(self):
        return re.split("=", self.currentCommand)[0]
    def comp(self):
        matches = re.findall("J?[01!&\-\+\|AMD]+=?", self.currentCommand)
        for x in matches:
            if re.search("=|J", x):
                pass
            else:
                return x
        

input_tuple = ("A=D+A", "@3", "(0010011101101100)", "junk")
x = Parser(input_tuple)


x.showCurrent()
print(x.commandType())
print(x.comp())

