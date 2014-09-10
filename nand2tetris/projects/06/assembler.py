# Assembles .asm files into machine code

import re

class Parser:
    def __init__(self, input_tuple):
        self.commands = len(input_tuple)
        self.currentPosition = 0
        self.currentCommand = input_tuple[0]
        self.lead_bits = '000'
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
        elif re.match("\(", self.currentCommand):
            return "L_COMMAND"
        else:
            self.lead_bits = '111'
            return "C_COMMAND"
    def dest(self):
        return re.findall("[AMD]+=", self.currentCommand)[0].replace("=", "") or ''
    def comp(self):
        matches = re.findall("J?[01!&\-\+\|AMD]+=?", self.currentCommand)
        for x in matches:
            if re.search("=|J", x):
                pass
            else:
                return x
    def jump(self):
        x = ''
        if re.search("J[\w]{2}", self.currentCommand):
            x = re.findall("J[\w]{2}", self.currentCommand)[0]
        return x

class Code:
    def __init__(self, parser):
        self.destCommand = parser.dest()
        self.compCommand = parser.comp()
        self.jumpCommand = parser.jump()

    def dest(self):
        commands = ['A', 'D', 'M']
        bits = ['0', '0', '0']
        for i, x in enumerate(commands):
            if re.search(x, self.destCommand):
                bits[i] = '1'
        return ''.join(bits)

    def comp(self):
        print(self.compCommand)
        lead_bit = '1' if re.search('M', self.compCommand) else '0'
        command = self.compCommand.replace('A', 'X').replace('M', 'X')
        bits = {
        "0" : '101010',
        "1" : '111111',
        "-1" : '111010',
        "D" : '001100',
        "X" : '110000',
        "!D" : '001101',
        "!X" : '110001',
        "-D" : '001111',
        "-X" : '110011',
        "D+1" : '011111',
        "X+1" : '110111',
        "D-1" : '001110',
        "X-1" : '110010',
        "D+X" : '000010',
        "D-X" : '010011',
        "X-D" : '000111',
        "D&X" : '000000',
        "D|X" : '010101'
        }
        return lead_bit + bits[command]

    def jump(self):
        bits = {
        ''    : '000',
        'JGT' : '001',
        'JEQ' : '010',
        'JGE' : '011',
        'JLT' : '100',
        'JNE' : '101',
        'JLE' : '110',
        'JMP' : '111'
        }
        return bits[self.jumpCommand]




input_tuple = ("M=0", "@3", "(0010011101101100)", "junk")
x = Parser(input_tuple)
y = Code(x)

print(x.commandType())

print(x.jump())
print(x.lead_bits + y.comp() + y.dest() + y.jump())

