names = open("name.basics.tsv")
akas = open("title.akas.tsv")
princ = open("title.principals.tsv")

class Actor:
	def __init__(self, name, apn):
		self.name = name
		self.apn = apn

class Movie:
	def __init__(self, name, apn):
		self.name = name
		self.apn = apn
		self.actors = []

	def add_actor(self, actor):
		self.actors.push(actor)

actors = {}
movies = {}

print("parsing actors")

for line in names:
	tokens = line.split("	")
	apn = tokens[0]
	name = tokens[1]
	actors[apn] = Actor(name, apn)

print("parsing titles")

for line in akas:
	tokens = line.split("	")
	apn = tokens[0]
	name = tokens[2]
	movies[apn] = Movie(name, apn)

print("linking")

for line in principals:
	tokens = line.split("	")
	movie = tokens[0]
	actor = tokens[2]

	if tokens[3] in ["actor", "actress"]:
		movies[movie].add_actor(actor)

print("finished!")
