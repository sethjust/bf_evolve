#!/usr/bin/python

import re, sys

class CompileError(Exception):
	def __init__(self):
		pass
	def __str__(self):
		return repr(self.value)

class BF_Machine(object):
	def __init__(self, program):
		self.jump_stack = []

		try:
			self.first_instruction = self.compile(program)
		except CompileError:
			raise CompileError

		self.cur_instruction = self.first_instruction
		self.prev_instruction = None
		
		MEMORY_SIZE = 32768
#		MEMORY_SIZE = 20
		
		self.first_cell = BF_Cell(None,None,0)
		self.cur_cell = self.first_cell

		for i in range(0, MEMORY_SIZE):
			mem = BF_Cell(self.cur_cell,None,0)
			self.cur_cell.next = mem
			self.cur_cell = mem

		self.cur_cell.next = self.first_cell
		self.first_cell.prev = self.cur_cell

		self.cur_cell = self.first_cell

		self.output = []

	def compile(self, program):
		instruction = None
		while True:
			if program == []:
				break
			char = program.pop()

			loop = None

			instruction = BF_Instruction(self, char, instruction, loop)

			if char == ']':
				self.jump_stack.append(instruction)
			if char == '[':
#				if self.jump_stack == []:
#					raise CompileError
				loop = self.jump_stack.pop()

			if not loop == None:
				instruction.loop = loop
				loop.loop = instruction
			
#		if not self.jump_stack == []:
#			raise CompileError
		return instruction
	def run(self, max_steps=10000):
		self.cur_instruction = self.first_instruction
		steps = 0
		while True:
			steps = steps + 1
			if steps > max_steps: return self.output
			self.cur_instruction.run()
			self.prev_instruction = self.cur_instruction
			self.cur_instruction = self.cur_instruction.next_instruction
			if self.cur_instruction == None:
				break
		return self.output
	def increment(self):
		self.cur_cell.value += 1
		self.cur_cell.value = self.cur_cell.value % 256
	def decrement(self):
		self.cur_cell.value -= 1
		self.cur_cell.value = self.cur_cell.value % 256
	def left(self):
		self.cur_cell = self.cur_cell.next
	def right(self):
		self.cur_cell = self.cur_cell.prev
	def display(self):
	  self.output.append(chr(self.cur_cell.value))
	def fwd(self):
		if self.cur_cell.value == 0:
			self.cur_instruction = self.cur_instruction.loop
	def bkwd(self):
		if not self.cur_cell.value == 0:
			self.cur_instruction = self.cur_instruction.loop
	def input(self):
		input = 0
		while not input:
			input = sys.stdin.read(1)
		self.cur_cell.value = ord(input)

class BF_Instruction(object):
	def __init__(self, machine, char, next_instruction, loop):
		self.machine = machine
		self.cmd = char
		self.next_instruction = next_instruction
		self.loop = loop

		if self.cmd == '+':
			self.run_func = lambda: self.machine.increment()
		if self.cmd == '-':
			self.run_func = lambda: self.machine.decrement()
		if self.cmd == '<':
			self.run_func = lambda: self.machine.left()
		if self.cmd == '>':
			self.run_func = lambda: self.machine.right()
		if self.cmd == '[':
			self.run_func = lambda: self.machine.fwd()
		if self.cmd == ']':
			self.run_func = lambda: self.machine.bkwd()
		if self.cmd == '.':
			self.run_func = lambda: self.machine.display()
		if self.cmd == ',':
			self.run_func = lambda: self.machine.input()
	def run(self):
		self.run_func()
	def dump(self):
		print self.cmd, self, self.loop

class BF_Cell(object):
	def __init__(self, prev, next, value):
		self.next = next
		self.prev = prev
		self.value = value

def run(prog_string):
	program = re.findall(r"[<>+-\.\[\]]", prog_string)

	try:
		machine = BF_Machine(program)
	except CompileError:
		print 'Compile Error'
		sys.exit()

	return machine.run()

if __name__ == '__main__':
	input = ''.join(sys.stdin.readlines())
	run(input)
