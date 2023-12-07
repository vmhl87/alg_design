# arithmetic_expression.py
# GOAL: Implements two stack algorithm to evaluate infix arithmetic expressions
# Code Author: Vincent Loh

# Stack class - uses internal linked list for performance
# size() and isEmpty() are unnecessary so they have been removed
class Stack:
	def __init__(self):
		self._start = False

	class Node:
		def __init__(self, item):
			self.item = item
			self.next = False

	def push(self, item):
		if self._start:
			tmp = self.Node(item)
			tmp.next = self._start
			self._start = tmp
		else:
			self._start = self.Node(item)

	def pop(self):
		if self._start:
			tmp = self._start.item
			self._start = self._start.next
			return tmp
		return False

	def peek(self):
		if self._start:
			return self._start.item
		return False

# Tokenizer class similar to Java's StringTokenizer() - splits a string
# into a series of integers or operator tokens
class Tokenizer:
	# Internally uses a Stack to store sub-tokens (characters in string)
	def __init__(self, expression):
		# internal expression stack
		self._expression = Stack()

		# defined set of operators (False is included so that when the
		# expression Stack is empty, the search loop will finish
		self._ops = ['(', ')', '+', '*', '/', '-', ' ', False]

		lastIsDigit = False

		# loop backwards through characters in string
		for index in range(len(expression)):
			char = expression[-(index + 1)]

			# if the character is an operator, push it
			if char in self._ops:
				self._expression.push(char)

				lastIsDigit = False

			# otherwise, check if the last value pushed was an
			# integer, and if so, compound the current char
			else:
				if lastIsDigit:
					# expanded for readability
					self._expression.push(int(
						char+str(self._expression.pop())
					))
				else:
					self._expression.push(int(char))

				lastIsDigit = True

	def nextToken(self):
		return self._expression.pop()

	def listTokens(self):
		tokens = []

		while True:
			token = self.nextToken()

			if not token:
				break

			tokens.append(token)

		return tokens

# simple utilities
def isArithmeticOperator(token):
	return token in [char for char in "+-*/"]

def isDigit(token):
	for char in str(token):
		if not char in "0123456789":
			return False
	return True

# due to a quirk in the way that this algorithm orders the numbers when
# evaluating, in a subtraction or division operation, we must swap the
# two operands (ex. divide the 2nd to top operand by the top one)
def performArithmeticOperation(operator, operand2, operand1):
	# error handling
	if not operand1 or not operand1:
		print("    Unbalanced arithmetic operation - double-check "+
			"that each group of parentheses has exactly two "+
			"elements inside it, and one operator")

		# mess of ternary operator that returns the non-false value
		# if it exists otherwise 0
		return operand1 if operand1 else (operand2 if operand2 else 0)

	if operator == '+':
		return operand1 + operand2

	elif operator == '-':
		return operand1 - operand2

	elif operator == '*':
		return operand1 * operand2

	elif operator == '/':
		return operand1 / operand2

# takes in an infixed arithmetic expression as a string and evaluates it with
# the two stacks algorithm
def evaluate(expression):
	# create our stacks
	operands = Stack()
	operators = Stack()
	
	# create tokenizer
	tokenizer = Tokenizer(expression)

	# Technically this is bad practice, but tokenizer will empty at some
	# finite point in time, causing the loop to exit - infinite loop
	# scenario is impossible here
	while True:
		# get next token
		token = tokenizer.nextToken()

		# if Tokenizer returns False when all of its sub-tokens
		# have been emptied, meaning we have finished parsing the
		# expression
		if not token:
			break

		# if token is an operator, push to operation stack
		if isArithmeticOperator(token):
			operators.push(token)

		# if token is end parenthesis, evaluate by manipulating the
		# operand stack
		elif token == ')':
			operator = operators.pop()

			# expanded for readability
			operands.push(
				performArithmeticOperation(
					operator,
					operands.pop(),
					operands.pop()
				)
			)

		# otherwise if token is an int, push to operand stack
		elif isDigit(token):
			operands.push(token)

	# return last value in operand stack (which also empties it)
	return operands.pop()
