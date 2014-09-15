# Assembles .asm files into machine code

import sys
import re

j = open(sys.argv[1], "r")
k = re.sub("\..+$", "", j.name)
o = open(k + ".hack", "w+")

input_lines = []
for line in j:
    input_lines.append(line.replace("\n", ""))

class Parser:
    def __init__(self, input_lines):
        self.commands = len(input_lines)
        self.currentPosition = 0
        self.currentCommand = input_lines[0]
        self.lead_bits = '000'
    def advance(self):
        self.currentPosition += 1
        self.currentCommand = input_lines[self.currentPosition]
    def reset(self):
        self.currentPosition = 0
        self.currentCommand = input_lines[self.currentPosition]
    def showCurrent(self):
        print(self.currentCommand)
    def hasMoreCommands(self):
        if self.currentPosition + 1>= self.commands:
            return False
        return True
    def commandType(self):
        command = self.currentCommand
        if re.match("^[\s]*//", command) or re.search("^\s*$", command):
            pass #current line is a blank line or comment
        elif re.search("^[\s]*@", command):
            return "A_COMMAND"
        elif re.search("^[\s]*\(", command):
            return "L_COMMAND"
        else:
            self.lead_bits = '111'
            return "C_COMMAND"
    def dest(self):
        if re.search("[AMD]+=", self.currentCommand):
            return re.findall("[AMD]+=", self.currentCommand)[0].replace("=", "")
        return ''
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
        lead_bit = '1' if re.search('M', self.compCommand) else '0'
        command = self.compCommand.replace('A', 'X').replace('M', 'X')
        bits = {
            "0"   : '101010',
            "1"   : '111111',
            "-1"  : '111010',
            "D"   : '001100',
            "X"   : '110000',
            "!D"  : '001101',
            "!X"  : '110001',
            "-D"  : '001111',
            "-X"  : '110011',
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

class SymbolTable:
    def __init__(self):
        self.table = {
        "SP"     : 0,
        "LCL"    : 1,
        "ARG"    : 2,
        "THIS"   : 3,
        "THAT"   : 4,
        "R0"     : 0,
        "R1"     : 1,
        "R2"     : 2,
        "R3"     : 3,
        "R4"     : 4,
        "R5"     : 5,
        "R6"     : 6,
        "R7"     : 7,
        "R8"     : 8,
        "R9"     : 9,
        "R10"    : 10,
        "R11"    : 11,
        "R12"    : 12,
        "R13"    : 13,
        "R14"    : 14,
        "R15"    : 15,
        "SCREEN" : 16384,
        "KBD"    : 24576
        }
    def addEntry(self, symbol, address):
        self.table[symbol] = address
    def contains(self, symbol):
        if symbol in self.table:
            return True
        return False
    def getAddress(self, symbol):
        return self.table[symbol]

x = Parser(input_lines)
symTable = SymbolTable()

def passOne(input_lines, x, symTable):
    count = 0
    for i in input_lines:
        type = x.commandType()

        if type in ['C_COMMAND','A_COMMAND']:
            count += 1

        if type == 'L_COMMAND':
            symbol = re.findall("[^\(\)]+", x.currentCommand)[0]
            symTable.table[symbol] = count

        if x.hasMoreCommands():
            x.advance()

def passTwo(input_lines, x, symTable):
    x.reset()
    nextAddress = 16
    for i, c in enumerate(input_lines):
        type = x.commandType()
        if type == 'C_COMMAND':
            y = Code(x)
            instruction = x.lead_bits + y.comp() + y.dest() + y.jump()
            o.write(instruction + "\n")

        if type == 'A_COMMAND':
            command = re.findall("[^@\s]+", c)[0]
            try:
                command = int(command)
            except ValueError:
                if command not in symTable.table:
                    symTable.addEntry(command, nextAddress)
                    nextAddress += 1
                command = int(symTable.table[command])

            instruction = format(command, "016b")
            o.write(instruction + "\n")

        if x.hasMoreCommands():
            x.advance()

passOne(input_lines, x, symTable)
passTwo(input_lines, x, symTable)
