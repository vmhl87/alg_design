from heap import Heap
import random
import sys

n = 15
p1 = 1
p2 = 0.3

if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
    except:
        print("demo.py <nodes> <step> <pause>")
        exit()
if len(sys.argv) > 2: p1 = float(sys.argv[2])
if len(sys.argv) > 3: p2 = float(sys.argv[3])

a = [1+(i%9) for i in range(0, n)]

random.shuffle(a)

h = Heap(p1, p2)

for i in a:
    h.push(i)

while not h.empty():
    h.pop()
