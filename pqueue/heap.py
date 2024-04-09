# interface with custom container datastructure
from container import Container, Status

# Binary Heap datastructure that internally uses a
# Container class for item storage and access, which
# can display changes in real time.
# Methods are kept semi-consistent with c++ STL
# - empty(), size(): self explanatory
# - _prop(i): upwards propagation from node i  [[internal]]
# - push(item): append item to heap and reheapify
# - pop(): remove top item and reheapify
# - top(): return top item
class Heap:
    def __init__(self):
        self._tree = Container()

    # utilities
    def empty(self): return self._tree.size() == 1
    def size(self): return self._tree.size() - 1

    # upwards propagation (SWIM)
    def _prop(self, i):
        # until we reach the root, or no longer have
        # to keep SWIMming upwards, compare and swap
        while i > 1:
            s = "Compare \033[0;33m" + str(self._tree.get(i))
            s += "\033[0m with \033[0;33m" + str(self._tree.get(i//2))
            s += "\033[0m"
            Status(s)
            if self._tree.compare(i, i//2):
                s = "Promote \033[0;36m" + str(self._tree.get(i))
                s += "\033[0m upwards"
                Status(s)
                self._tree.swap(i, i//2)
                i //= 2
            else:
                break

    # push and reheapify (because we append item to
    # the end of the tree we do not need to SINK)
    def push(self, item):
        Status("Add \033[0;32m" + str(item) + "\033[0m to heap")
        self._tree.push(item)
        self._prop(self._tree.size() - 1)

    # refill tree from list and reheapify
    def fill(self, items):
        Status("Clear heap")
        self._tree = Container()
        for item in items:
            Status("Add \033[0;32m" + str(item) + "\033[0m to heap")
            self._tree.push(item)
        self.rebalance()

    # reheapify
    def rebalance(self):
        for i in range(2, self._tree.size()):
            self._prop(i)

    # essentially just a wrapper
    def top(self):
        if self._tree.size() == 1: return None
        return self._tree.get(1)

    # downwards propagation (SINK) from the root
    def pop(self):
        if self._tree.size() == 1: return
        # we set the root to 'x' to make it clearer in
        # the visualization that we are deleting
        Status("\033[0;31mRemove\033[0m root node")
        self._tree.set(1, "\033[0;31mx\033[0m")
        # the location of the hole, i, starts at 1
        i = 1
        # continually pick the smaller child of the hole
        # and swap them
        while i*2 < self._tree.size():
            Status("Choose \033[0;33mchild\033[0m to promote")
            if self._tree.compare(i*2, i*2+1):
                Status("Promote \033[0;36mleft\033[0m child")
                self._tree.swap(i, i*2)
                i = i*2
            else:
                Status("Promote \033[0;36mright\033[0m child")
                self._tree.swap(i, i*2+1)
                i = i*2+1
        # we don't want hanging holes, because it messes
        # up contiguity, so if necessary we swap end with hole
        if i != self._tree.size() - 1:
            s = "Swap \033[0;31mhole\033[0m with \033[0;36m"
            s += "last\033[0m element"
            Status(s)
            self._tree.swap(i, self._tree.size() - 1)
            Status("\033[0;31mRemove\033[0m")
            self._tree.pop()
            self._prop(i)
        else:
            Status("\033[0;31mRemove\033[0m")
            self._tree.pop()
