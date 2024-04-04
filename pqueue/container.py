import time
import math

# Container datastructure that wraps a List and
# provides all necessary operations for binary
# heap to function, while adding a visual display.
#   size(): self explanatory
#   compare(a, b): find smaller of two items
#   swap(a, b): swap two items in the list
#   push(item): append item to end of list
#   pop(): remove item from end of list
#   get(i): get item at index i
#   set(i, v): set item at i with value v
#   draw(): draw tree
class Container:
    # _items initializes with a zero element because
    # the first element of the tree is indexed as 1
    def __init__(self):
        self._items = [0]
        # highlighted items
        self._color = [-1, -1]
        self._highlight = "37"
        self.draw()

    # animated wrappers
    def push(self, item):
        self._items.append(item)
        self._color[0] = len(self._items) - 1
        self._highlight = "32"
        self.draw()
        time.sleep(1)
        self._color[0] = -1
        self._highlight = "37"
        self.draw()
        time.sleep(0.3)

    def pop(self):
        self._color[0] = len(self._items) - 1
        self._highlight = "31"
        self.draw()
        time.sleep(1)
        self._color[0] = -1
        self._highlight = "37"
        self._items.pop()
        self.draw()
        time.sleep(0.3)

    def set(self, i, v):
        self._color[0] = i
        self._highlight = "31"
        self.draw()
        self._items[i] = v
        time.sleep(0.5)
        self.draw()
        time.sleep(0.5)
        self._color[0] = -1
        self._highlight = "37"
        self.draw()
        time.sleep(0.3)

    def get(self, i): return self._items[i]
    def size(self): return len(self._items)
    
    # due to the implementation of our top-down
    # propagation we must enforce a bounds check
    def compare(self, a, b):
        if b >= len(self._items): return True
        if a >= len(self._items): return False
        self._color = [a, b]
        self._highlight = "33"
        self.draw()
        time.sleep(1)
        self._color = [-1, -1]
        self._highlight = "37"
        self.draw()
        time.sleep(0.3)
        return self._items[a] < self._items[b]

    # animated swap
    def swap(self, a, b):
        self._color = [a, b]
        self._highlight = "36"
        self.draw()
        t = self._items[a]
        self._items[a] = self._items[b]
        self._items[b] = t
        time.sleep(0.5)
        self.draw()
        time.sleep(0.5)
        self._color = [-1, -1]
        self._highlight = "37"
        self.draw()
        time.sleep(0.3)

    # pretty print tree
    def draw(self):
        cat = ""
        nxt = 2
        spc = 1
        if len(self._items) > 1:
            spc = int(math.pow(2, int(math.log2(len(self._items)-1))))
        for _ in range(1, spc):
            cat += ' '
        for i in range(1, len(self._items)):
            if i == nxt:
                cat += '\n'
                spc //= 2
                for _ in range(1, spc):
                    cat += ' '
                nxt *= 2
            if i > nxt // 2:
                for _ in range(0, spc+spc-1):
                    cat += ' '
            cat += "\033[0;"
            if i in self._color:
                cat += self._highlight
            else:
                cat += "37"
            cat += 'm'
            cat += str(self._items[i])
            cat += "\033[0m"
        print(cat)
