# Basic binary heap - supports public methods push, pop, top
class Heap:
    def __init__(self, items=False):
        self._tree = [0]
        if items:
            self.push(items)

    # utilities - mantain semiconsistency with c++ STL
    def empty(self): return len(self._tree) == 1
    def size(self): return len(self._tree) - 1

    # pushdown - for a possibily violated node i, propagate up until fixed
    def _prop(self, i):
        while i > 1:
            if self._tree[i] < self._tree[i//2]:
                t = self._tree[i]
                self._tree[i] = self._tree[i//2]
                self._tree[i//2] = t
                i //= 2
            else: break

    # append a new element to the end of the heap and re-heapify
    def push(self, item):
        # allow pushing many elements at a time
        if type(item) == list:
            for i in item: self.push(i)
        else:
            self._tree.append(item)
            self._prop(len(self._tree) - 1)

    # very simple, return first element if it exists
    def top(self):
        if len(self._tree) == 1: return None
        return self._tree[1]

    # remove largest element, creating a hole, then propagate hole down
    def pop(self):
        if len(self._tree) == 1: return
        i = 1 # hole starts at index 1
        while i*2 < len(self._tree):
            if i*2+1 < len(self._tree):
                if self._tree[i*2] < self._tree[i*2+1]:
                    self._tree[i] = self._tree[i*2]
                    i *= 2
                else:
                    self._tree[i] = self._tree[i*2+1]
                    i = i*2+1
            else:
                self._tree[i] = self._tree[i*2]
                i *= 2
        # mantain contiguity by swapping end of heap with hole
        if i != len(self._tree) - 1:
            self._tree[i] = self._tree[len(self._tree) - 1]
            self._prop(i)
        self._tree.pop()
