from heap import Heap
import random

def heapsort(arr):
    heap = Heap(0.5, 0.2)
    for i in arr:
        heap.push(i)
    ret = []
    while not heap.empty():
        ret.append(heap.top())
        heap.pop()
    return ret

a = [i for i in range(1, 9)]

random.shuffle(a)

b = heapsort(a)

print("a: " + str(a))
print("b: " + str(b))
