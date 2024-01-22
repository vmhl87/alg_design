from graph import Graph
from stack import Stack

# setup example graph

g = Graph(9)

edges = [
	[0, 1],
	[0, 8],
	[8, 2],
	[2, 3],
	[2, 4],
	[4, 7],
	[7, 6],
	[6, 5],
	[8, 6],
	[2, 5]
]

for edge in edges:
	g.addEdge(edge[0], edge[1])

node_names = ["a", "b", "c", "d", "e", "f", "g", "h", "s"]

# setup stack

s = Stack()

# dfs!

class dfs_node:
	def __init__(self, iterator):
		self.items = iterator

		self.index = 0

		self.done = False

	def update(self):
		if self.done: return False

		ret = self.items[self.index]

		self.index += 1

		if self.index == len(self.items):
			self.done = True

		return ret

s.push(dfs_node(g.adjList(0)))

print("a")

visited = [False for i in range(9)]

visited[0] = True

while not s.isEmpty():
	next = s.peek().update()

	if next:
		if not visited[next.id]:
			print(node_names[next.id])

			s.push(dfs_node(g.adjList(next.id)))

			visited[next.id] = True

	else:
		s.pop()
