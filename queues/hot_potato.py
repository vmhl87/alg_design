class Queue:
	def __init__(self):
		self._start = False
		self._end = False
		self._size = 0

	class Node:
		def __init__(self, item):
			self.item = item
			self.next = False

	def enqueue(self, item):
		self._size += 1
		if self._end:
			tmp = self.Node(item)
			self._end.next = tmp
			self._end = tmp
			if not self._start:
				self._start = tmp
		else:
			self._start = self.Node(item)
			self._end = self._start

	def dequeue(self):
		if self._start:
			self._size -= 1;
			tmp = self._start.item
			self._start = self._start.next
			return tmp
		return False

	def peek(self):
		if self._end:
			return self._end.item
		return False

	def size(self):
		return self._size

	def isEmpty(self):
		if self._start: return False
		return True

def hotPotato(namelist, number):
#	for i in range(number+1):
#		print(namelist[i % len(namelist)])
	q = Queue()
	for name in namelist:
		q.enqueue(name)
	for i in range(number):
		tmp = q.dequeue()
		q.enqueue(tmp)
		print(tmp)
	print("Result: " + q.dequeue())
