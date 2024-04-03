from heap import Heap

def heapsort(arr):
    heap = Heap(arr)
    ret = []
    while not heap.empty():
        ret.append(heap.top())
        heap.pop()
    return ret
