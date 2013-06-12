import sys
import collections

class Brainfuck:

    def __init__(self):
        self.cells = [0] * 9999
        self.pointer = 0
        self.stack_pointer = 0
        self.has_error = False
        
        self.source = None
        self.tokens = []

    def load(self, filename):
        try:
            self.source = open(filename, "r")
        except IOError:
            print "Error loading source"

        self.source = self.source.read()
        self.tokens = self.tokenize()

        self.interpret(self.tokens)

    def tokenize(self):
        tokens = []

        while self.stack_pointer < len(self.source):
            char = self.source[self.stack_pointer]

            if char in [',', '.', '>', '<', '+', '-']:
                tokens.append(char)
            elif char == '[':
                self.stack_pointer += 1
                sub_token = self.tokenize()
                tokens.append(sub_token)
            elif char == ']':
                break

            self.stack_pointer += 1

        return tokens


    def interpret(self, tokens):
        stack_pointer = 0

        while stack_pointer < len(tokens):
            if self.has_error:
                return

            char = tokens[stack_pointer]

            if   char == ',':
                self.input()
            elif char == '.':
                self.output()
            elif char == '>':
                self.next_cell()
            elif char == '<':
                self.previous_cell()
            elif char == '+':
                self.increase_cell()
            elif char == '-':
                self.decrease_cell()
            elif isinstance(char, collections.Iterable):
                while self.current_cell_not_zero(): 
                    self.interpret(char)
                
            stack_pointer += 1


    def current_cell_not_zero(self):
        return self.cells[self.pointer] != 0

    def input(self):
        self.cells[self.pointer] = ord(raw_input()[0])

    def output(self):
        sys.stdout.write(chr(self.cells[self.pointer]))

    def next_cell(self):
        if self.pointer == len(self.cells): 
            self.error("No more cells ahead")
            return

        self.pointer += 1


    def previous_cell(self):
        if self.pointer == 0: 
            self.error("This is the first cell already")
            return

        self.pointer -= 1

    def increase_cell(self):
        self.cells[self.pointer] += 1

    def decrease_cell(self):
        self.cells[self.pointer] -= 1


    def error(self, message):
        print("### ERROR: %s" % message)
        self.has_error = True
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
            \npybf.py -- no file specified. how to use: 
            \n\t$ python pybf.py sourcefile\n""")
    else:
        bf = Brainfuck()
        bf.load(sys.argv[1])