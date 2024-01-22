class Graph:
	def __init__(self, v):
		self.nodes = [self.Node(i) for i in range(v)]

	def addEdge(self, n1, n2, directed=False):
		self.nodes[n1].add(self.nodes[n2])

		if not directed:
			self.nodes[n2].add(self.nodes[n1])

	def adjList(self, v, ids=False):
		return self.nodes[v].adj.list(ids)
		# return self.AdjListIterator(self.nodes[v].adj)

	class AdjListIterator:
		def __init__(self, AdjList):
			self._node = AdjList._start

		def __iter__(self):
			return self

		def __next__(self):
			if self._node:
				tmp = self._node.to

				self._node = self._node.next

				return tmp

			else:
				raise StopIteration

				return False

	class Node:
		def __init__(self, id):
			self.adj = self.AdjList()
			self.id = id

		def add(self, other):
			self.adj.add(other)

		class AdjList:
			def __init__(self):
				self._start = None
				self._end = None

			def list(self, ids=False):
				ret = []

				node = self._start
				while node:
					if ids:
						ret.append(node.to.id)
					else:
						ret.append(node.to)
					node = node.next
				return ret

			def add(self, other):
				tmp = self.EdgeNode(other)

				if not self._start:
					self._start = tmp

				if self._end:
					self._end.link(tmp)

				self._end = tmp

			class EdgeNode:
				def __init__(self, to):
					self.to = to
					self.next = None

				def link(self, next):
					self.next = next
