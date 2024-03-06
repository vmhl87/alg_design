from heuristic import PageDistance

# maximum order size because we have limited examples
classifier = PageDistance("fish", depth=9, order_size=30)

print("classifier init")

distances = classifier.distances([
    "whale",
    "overfishing",
    "ocean acidification",
    "salmon",
    "glass",
    "crab"
])

for distance in distances:
    print(distance['page'] + " was predicted to be " + str(round(distance['distance'],4)) + " away from fish")
