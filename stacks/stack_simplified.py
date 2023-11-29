class Stack:
	def __init__(self):
		self._items = []

	def isEmpty(self):
		return len(self._items) == 0

	def push(self, item):
		#self._items.append(item)
		self._items.insert(0, item)

	def pop(self):
		#return self._items.pop()
		return self._items.pop(0)

	def peek(self):
		#return self._items[-1]
		return self._items[0]

	def size(self):
		return len(self._items)

def reverseWord(word):
	st = Stack()

	for char in word:
		st.push(char)

	ret = ""

	for char in word:
		ret += st.pop()

	return ret

def stripped(word):
	lowercase = word.lower()
	
	alphabet = [char for char in "abcdefghijklmnopqrstuvwxyz"]

	ret = ""

	for char in lowercase:
		if char in alphabet:
			ret += char

	return ret

def isPalindrome(word):
	reversed = reverseWord(word)

	return stripped(word) == stripped(reversed)
