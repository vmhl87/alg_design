# reverse_words.py
# GOAL: use a Stack to reverse the characters of a string, and then use this to detect palindromes
# Code Author: Vincent Loh

# Stack class - uses an internal array
class Stack:
	# constructor
	def __init__(self):
		self._items = []

	# methods
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

# To reverse the characters of a word, we will push them onto the stack one by one and then
# pop them off, reversing the order
def reverseWord(word):
	# allocate a Stack() object
	st = Stack()

	# iterate through the characters of `word`
	for char in word:
		st.push(char)

	# temporary string to return
	ret = ""

	# while there is an item in the stack
	while not st.isEmpty():
		ret += st.pop()

	return ret

# strip non-alphabetic characters from a string
def stripped(word):
	# make everything lowercase
	lowercase = word.lower()
	
	# create char array of allowed chars
	alphabet = [char for char in "abcdefghijklmnopqrstuvwxyz"]

	# return string
	ret = ""

	# loop through each character of the word, and add it to `ret` when
	# it is in library of allowed characters
	for char in lowercase:
		if char in alphabet:
			ret += char

	return ret

# find if a word is a palindrome
def isPalindrome(word):
	# reverse the word
	reversed = reverseWord(word)

	# check if word == reversed word
	return stripped(word) == stripped(reversed)

# ----------- tests -----------

tests = [
	["hello world", "reverse"],
	["go hang a salami, I'm a lasagna hog", "palindrome"],
	["this is not a palindrome", "palindrome"]
]

print("Tests:")

for test in tests:
	if test[1] == "reverse":
		print("The reverse of `" + test[0] + "` is `" + reverseWord(test[0]) + "`")
	else:
		print("`" + test[0] + "` " + ("is" if isPalindrome(test[0]) else "is not") + " a palindrome")

print("Type in a word you want to reverse or check if it is a palindrome, or `exit` to exit")

word = ""

while True:
	word = input(">>> ")

	if word == "exit": break

	if input("Check if word is palindrome? (y/n) ") == "y":
		print("`" + word + "` " + ("is" if isPalindrome(word) else "is not") + " a palindrome")
	else:
		print("The reverse of `" + word + "` is `" + reverseWord(word) + "`")
