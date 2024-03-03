from heuristic import PageDistance

classifier = PageDistance("Bob", depth=9, order_size=5)

distances = classifier.distances([
    "Bob's neighbor",
    "The kid two doors down the street from Bob",
    "A friend of Bob",
    "A friend of Bob's neighbor's friend who is neighbors with Bob",
    "Someone who doesn't know Bob or met him at all",
    "A random stranger who has never met Bob in their life"
])

for distance in distances:
    print(distance['page'] + " was predicted to be " + str(round(distance['distance'],4)) + " away from Bob")
