import sys

class Brainfuck:

	def __init__(self):
		self.cells = [0 for i in range(9999)]
		self.pointer = 0
		self.sp = 0
		self.loop = []
		self.has_error = False

	def load(self, filename):
		try:
			self.source = open(filename, "r")
		except IOError:
			print "Error loading source"

		self.interpret()

	def interpret(self):
		self.source = self.source.read()

		while self.sp < len(self.source):
			if self.has_error:
				return

			c = self.source[self.sp]

			if   c == ',':
				self.input()
			elif c == '.':
				self.output()
			elif c == '>':
				self.next_cell()
			elif c == '<':
				self.previous_cell()
			elif c == '+':
				self.increase_cell()
			elif c == '-':
				self.decrease_cell()
			elif c == '[':
				self.start_loop()
			elif c == ']':
				self.resume_loop()
				
			self.sp += 1



	def input(self):
		self.cells[self.pointer] = ord(raw_input()[0])

	def output(self):
		print(chr(self.cells[self.pointer]))

	def next_cell(self):
		if self.pointer == len(self.cells): 
			self.error("No more cells ahead")
			return;

		self.pointer += 1


	def previous_cell(self):
		if self.pointer == 0: 
			self.error("This is the first cell already")
			return;

		self.pointer -= 1

	def increase_cell(self):
		self.cells[self.pointer] += 1

	def decrease_cell(self):
		self.cells[self.pointer] -= 1

	def start_loop(self):
		print("start_loop")

	def resume_loop(self):
		print("resume_loop")


	def error(self, message):
		print("### ERROR: %s" % message)
		self.has_error = True
		

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("\npybf.py -- no file specified. how to use: \n\t$ python pybf.py sourcefile\n")
	else:
		bf = Brainfuck()
		bf.load(sys.argv[1])