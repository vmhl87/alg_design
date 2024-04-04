from container import Container

# Binary Heap datastructure that internally uses a
# Container class for item storage and access, which
# can display changes in real time.
# Methods are kept semi-consistent with c++ STL
#   empty(), size(): self explanatory
#   _prop(i): upwards propagation from node i
#   push(item): append item to heap and reheapify
#   pop(): remove top item and reheapify
#   top(): return top item
class Heap:
    def __init__(self, p1=0.8, p2=0.2):
        self._tree = Container(p1, p2)

    # utilities
    def empty(self): return self._tree.size() == 1
    def size(self): return self._tree.size() - 1

    # upwards propagation (SWIM)
    def _prop(self, i):
        # until we reach the root, or no longer have
        # to keep SWIMming upwards, compare and swap
        while i > 1:
            if self._tree.compare(i, i//2):
                self._tree.swap(i, i//2)
                i //= 2
            else:
                break

    # push and reheapify (because we append item to
    # the end of the tree we do not need to SINK)
    def push(self, item):
        self._tree.push(item)
        self._prop(self._tree.size() - 1)

    # essentially just a wrapper
    def top(self):
        if self._tree.size() == 1: return None
        return self._tree.get(1)

    # downwards propagation (SINK) from the root
    def pop(self):
        if self._tree.size() == 1: return
        # we set the root to 0 to make it clearer in
        # the visualization that we are deleting
        self._tree.set(1, "\033[0;31mx\033[0m")
        # the location of the hole, i, starts at 1
        i = 1
        # continually pick the smaller child of the hole
        # and swap them
        while i*2 < self._tree.size():
            if self._tree.compare(i*2, i*2+1):
                self._tree.swap(i, i*2)
                i = i*2
            else:
                self._tree.swap(i, i*2+1)
                i = i*2+1
        # we don't want hanging holes, because it messes
        # up contiguity, so if necessary we swap end with hole
        if i != self._tree.size() - 1:
            self._tree.swap(i, self._tree.size() - 1)
            self._tree.pop()
            self._prop(i)
        else:
            self._tree.pop()
