import time
import math
import os

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
    def __init__(self, p1, p2):
        self._items = [0]
        # highlighted items
        self._color = [-1, -1]
        self._highlight = "37"
        self.p1 = p1
        self.p2 = p2
        self.draw()

    # animated wrappers
    def push(self, item):
        self._items.append(item)
        self._color[0] = len(self._items) - 1
        self._highlight = "32"
        self.draw()
        time.sleep(self.p1)
        self._color[0] = -1
        self._highlight = "37"
        self.draw()
        time.sleep(self.p2)

    def pop(self):
        self._items.pop()
        self.draw()
        time.sleep(self.p2)

    def set(self, i, v):
        self._color[0] = i
        self._highlight = "31"
        self.draw()
        self._items[i] = v
        time.sleep(self.p1/2)
        self.draw()
        time.sleep(self.p1/2)
        self._color[0] = -1
        self._highlight = "37"
        self.draw()
        time.sleep(self.p2)

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
        time.sleep(self.p1)
        self._color = [-1, -1]
        self._highlight = "37"
        self.draw()
        time.sleep(self.p2)
        return self._items[a] < self._items[b]

    # animated swap
    def swap(self, a, b):
        self._color = [a, b]
        self._highlight = "36"
        self.draw()
        t = self._items[a]
        self._items[a] = self._items[b]
        self._items[b] = t
        time.sleep(self.p1/2)
        self.draw()
        time.sleep(self.p1/2)
        self._color = [-1, -1]
        self._highlight = "37"
        self.draw()
        time.sleep(self.p2)

    # pretty print tree
    def draw(self):
        cat = ""
        nxt = 2
        spc = 1
        hi = 1
        he = os.get_terminal_size()[1] - 1
        hw = os.get_terminal_size()[0] // 2
        if len(self._items) > 1:
            spc = int(math.pow(2, 1+int(math.log2(len(self._items)-1))))
            hi = 2*int(math.log2(len(self._items) - 1))
            hw -= spc
        he -= hi
        if hw < 0:
            hw += spc
            he += hi
            cat += '\n' * (he//2 - 1)
            s = "Your terminal is too small!"
            cat += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            cat += s + '\n'
            s = "Current: " + str(os.get_terminal_size()[0]) + " x "
            s += str(os.get_terminal_size()[1])
            cat += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            cat += s + '\n'
            s = "Needs: " + str(spc + spc + 1) + " x " + str(hi)
            cat += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            cat += s + '\n'
            cat += '\n' * (he - he//2 - 2)
            print(cat)
            return
        cat += '\n' * (he//2)
        cat += ' ' * (spc+hw-1)
        for i in range(1, len(self._items)):
            if i == nxt:
                spc //= 2
                nxt *= 2
                cat += '\n'
                cat += ' ' * hw
                for j in range(i, len(self._items)):
                    if j == nxt: break
                    if [j, j//2] == self._color:
                        cat += "\033[0;" + self._highlight + 'm'
                    if [j//2, j] == self._color:
                        cat += "\033[0;" + self._highlight + 'm'
                    cat += (' ' if j%2 == 0 else '-') * (spc-1)
                    cat += ' '
                    cat += ('-' if j%2 == 0 else ' ') * (spc-1)
                    cat += " \033[0m"
                cat += '\n'
                cat += ' ' * (spc+hw-1)
            if i > nxt // 2:
                cat += ' ' * (spc+spc-1)
            cat += "\033[0;"
            if i in self._color:
                cat += self._highlight
            else:
                cat += "37"
            cat += 'm'
            cat += str(self._items[i])
            cat += "\033[0m"
        cat += '\n' * (he - he//2)
        print(cat)
