# Assembles .asm files into machine code

class Parser:
    def __init__(self, input_tuple):
        # openInputFile
            # returns input_array, each item of which is a line from the input file
        self.commands = len(input_tuple)
        self.currentPosition = 0
        self.currentCommand = input_tuple[0]
    def advance(self):
        self.currentPosition += 1
        self.currentCommand = input_tuple[self.currentPosition]
    def showCurrent(self):
        print(self.currentCommand)
    def hasMoreCommands(self):
        if self.currentPosition == self.commands - 1:
            return False
        return True

input_tuple = (1, 2, 3, 4, 5)
x = Parser(input_tuple)
x.advance()
x.advance()
x.advance()
x.advance()

x.showCurrent()
if x.hasMoreCommands():
    print('true!')
else:
    print('false!')

