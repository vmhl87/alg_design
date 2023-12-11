class Deque:
	def __init__(self):
		self._start = False
		self._end = False
		self._size = 0

	class Node:
		def __init__(self, item):
			self.item = item
			self.next = False
			self.prev = False

	def addFront(self, item):
		self._size += 1
		if self._start:
			tmp = self.Node(item)
			self._start.prev = tmp
			tmp.next = self._start
			self._start = tmp
			if not self._end:
				self._end = tmp
		else:
			self._start = self.Node(item)
			self._end = self._start

	def removeFront(self):
		if self._start:
			self._size -= 1
			if self._start.next:
				self._start.next.prev = False
			tmp = self._start.item
			self._start = self._start.next
			return tmp
		return False

	def addRear(self, item):
		self._size += 1
		if self._end:
			tmp = self.Node(item)
			self._end.next = tmp
			tmp.prev = self._end
			self._end = tmp
			if not self._start:
				self._start = tmp
		else:
			self._end = self.Node(item)
			self._start = self._end

	def removeRear(self):
		if self._end:
			self._size -= 1
			if self._end.prev:
				self._end.prev.next = False
			tmp = self._end.item
			self._end = self._end.prev
			return tmp
		return False

	def size(self):
		return self._size

	def isEmpty(self):
		if self._start: return False
		return True

dq = Deque()

while True:
	command = input(">>> ")

	if command == "STOP":
		break

	if command.startswith("enqueue"):
		command = command[8:]

		if command.endswith(")"):
			dq.addFront(command[:-1])
		else:
			print("Try again. Type 'STOP' to stop program.")

	elif command == "dequeue()":
		student = dq.removeRear()

		if student:
			print("Now seeing: " + student)
		else:
			print("There is no one to be seen.")
	else:
		print("Try again. Type 'STOP' to stop program.")
