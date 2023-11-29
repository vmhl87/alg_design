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

s = Stack()

print(s.isEmpty())

s.push(4)
s.push("dog")

print(s.peek())

s.push(True)

print(s.size())
print(s.isEmpty())

s.push(8.4)

print(s.pop())
print(s.pop())
print(s.size())
