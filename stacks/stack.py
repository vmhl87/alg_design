class Stack:
	def __init__(self):
		self._start = False
		self._size = 0

	class Node:
		def __init__(self, item):
			self.item = item
			self.next = False

	def push(self, item):
		self._size += 1
		if self._start:
			tmp = self.Node(item)
			tmp.next = self._start
			self._start = tmp
		else:
			self._start = self.Node(item)

	def pop(self):
		if self._start:
			self._size -= 1;
			tmp = self._start.item
			self._start = self.start.next
			return tmp
		return False

	def peek(self):
		if self._start:
			return self._start.item
		return False

	def size(self):
		return self._start

	def isEmpty(self):
		if self._start: return False
		return True
