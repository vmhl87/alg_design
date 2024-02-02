"""
	Disclaimer: Unless you have *a lot* of memory, this program
	probably won't run. Likely it'll hang on 'Opening files', possibly
	to the point of noticeably slowing down the rest of your computer.
	It could even cause a kpanic, and unexpectedly reboot. I don't know.
	
	I strongly suggest using the c++ version of this program as it is
	at least 100x faster and uses less memory. Also, its code is more
	interesting - my method of data representation is somewhat unorthodox,
	and it can't be appreciated in as abstracted of a language as Python is.
	
	I wasn't able to easily trim down the dataset - the average order of
	each vertex was high enough that data trimming either caused lots of
	completely disconnected regions, or big clumps of people who were all
	mutually connected. And manufacturing an equivalent dataset defeats
	the purpose of the excercise.
	
	However - if you *really really* want to run this, be my guest - just
	make sure to allocate a lot of swap space, configure your system to let
	python use several gigabytes of RAM, and close out of any running apps
	with unsaved work.
	
	Maybe say a prayer or two.
"""

class Node:
	def __init__(self, i):
		self.id = i
		self.adj = None
		self.init = False
	
	def fill(self, adj):
		self.adj = adj;
		self.init = True

class TraverseNode:
	def __init__(self, i, prev, is_actor):
		self.id = i
		self.prev = prev
		self.depth = prev.depth+1 if prev else 0
		self.is_actor = is_actor

def progress(p):
	print(f"{round(p/10)*10}% complete")

print("Initializing datastructures")

progress(0)

actor_namelist, movie_namelist = [], []
name_len, akas_len = 13205098, 38592396

progress(40)

actor_adjlist = [Node(i) for i in range(name_len)]

progress(70)

movie_adjlist = [Node(i) for i in range(akas_len)]

progress(100)

def actor_node(i, prev):
	return TraverseNode(i, prev, True)

def movie_node(i, prev):
	return TraverseNode(i, prev, False)

def search(first):
	if first: print("Enter the name of an actor, or 'exit' to exit:")
	
	actor = input("> ")
	
	if actor == "exit": return
	
	print(f"Searching for {actor} in namelist")
	
	actor_id = -1
	
	for i in range(name_len):
		if actor_namelist[i] == actor:
			actor_id = i
			break
		progress(i*100/name_len)
	
	if actor_id == -1:
		print(f"\nCouldn't find {actor} in namelist\n")
		search(False)
		return
		
	else:
		print(f"\nFound {actor} at index {actor_id}")
	
	print("Building search queue")
	
	search_queue = []
	front_index = 0
	
	actors_visited, movies_visited = set(), set()
	
	search_queue.append(TraverseNode(actor_id, None, True))
	actors_visited.add(actor_id)
	
	print("Moving through graph")
	
	iterations, depth = 0, 0
	front = search_queue[0]
	
	found_kevin_bacon = False
	if actor == "Kevin Bacon": found_kevin_bacon = True
	
	while not found_kevin_bacon and front_index < len(search_queue):
		front = search_queue[front_index]
		front_index += 1
		
		finished = False
		
		if front.is_act:
			if actor_adjlist[front.id].init:
				for movie_id in actor_adjlist[front.id]:
					if not movie_id in movies_visited:
						movies_visited.add(movie_id)
						search_queue.append(
							movie_node(actor_adjlist[front.id], front)
						)
		
		else:
			if movie_adjlist[front.id].init:
				for actor_id in movie_adjlist[front.id]:
					if not actor_id in actors_visited:
						actors_visited.add(actor_id)
						search_queue.append(
							actor_node(movie_adjlist[front.id], front)
						)
						
						if actor_id == 101:
							front = search_queue[-1]
							found_kevin_bacon = True
							finished = True
							break
		
		if finished: break
		
		if front.depth > depth:
			print(f"Depth {front.depth} ({front_index} iterations)")
			depth = front.depth
	
	if not found_kevin_bacon:
		print(f"\nCouldn't find a path from {actor} to Kevin Bacon.\n")
		search(False)
		return
	
	print("\nFound Kevin Bacon!")
	
	path = []
	
	while front.prev:
		path.append(front)
		
		front = front.prev
	
	print("Path:")
	
	print(actor, end="")
	
	while len(path) > 0:
		node = path.pop()
		
		if node.is_act:
			print(actor_namelist[node.id], end="")
			if node.id == 101: break
		
		else:
			print(f" --- ({movie_namelist[node.id]}) --> ", end="")
	
	print("\n")
	
	search(True)

print("Opening files")

act_name = open("actors_name.list").readlines()
act_adj = open("actors_adj.list").readlines()
mov_name = open("movies_name.list").readlines()
mov_adj = open("movies_adj.list").readlines()

progress(100)

print("Building adjacency lists")

for i in range(name_len):
	actor_adjlist[i].fill([int(i) for i in act_adj[i].strip().split(" ")[1:]])
	progress(i*100/(name_len+akas_len))

for i in range(akas_len):
	movie_adjlist[i].fill([int(i) for i in mov_adj[i].strip().split(" ")[1:]])
	progress((i+name_len+1)*100/(name_len+akas_len))

progress(100)

print("Reading names")

for i in range(name_len):
	actor_namelist.append(act_name[i].strip())
	progress(i*100/(name_len+akas_len))

for i in range(akas_len):
	movie_namelist.append(mov_name[i].strip())
	progress(i*100/(name_len+akas_len))

progress(100)

print("Closing files")

act_adj.close()
act_name.close()
mov_adj.close()
mov.name.close()

progress(100)

print("Ready")

search(True)

print("Exiting")
