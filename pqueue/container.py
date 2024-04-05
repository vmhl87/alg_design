# import necessary components
# - time necessary to pause
# - math necessary for log2
# - os necessary for terminal size info
import time
import math
import os

# Container datastructure that wraps a List and
# provides all necessary operations for binary
# heap to function, while adding a visual display.
# - size(): self explanatory
# - compare(a, b): find smaller of two items
# - swap(a, b): swap two items in the list
# - push(item): append item to end of list
# - pop(): remove item from end of list
# - get(i): get item at index i
# - set(i, v): set item at i with value v
# - draw(): draw tree  [[internal]]
class Container:
    # _items initializes with a zero element because
    # the first element of the tree is indexed as 1
    def __init__(self, p1, p2):
        self._items = [0]
        # highlighted items
        self._color = [-1, -1]
        # ANSI highlight color
        self._highlight = "37"
        # pause amounts
        self.p1 = p1
        self.p2 = p2
        # first draw
        self.draw()

    # animated push
    def push(self, item):
        self._items.append(item)
        # color the appended item green (ANSI 32)
        self._color[0] = len(self._items) - 1
        self._highlight = "32"
        # draw and wait
        self.draw()
        time.sleep(self.p1)
        # reset color and redraw
        self._color[0] = -1
        self.draw()
        # wait again (for next instruction)
        time.sleep(self.p2)

    # no animation
    def pop(self):
        self._items.pop()
        self.draw()
        time.sleep(self.p2)

    # the only time set() gets called is when marking the
    # rooot node for deletion - we automatically color red
    def set(self, i, v):
        # color node i red and draw
        self._color[0] = i
        self._highlight = "31"
        self.draw()
        # render half-frame to show change
        self._items[i] = v
        time.sleep(self.p1/2)
        self.draw()
        time.sleep(self.p1/2)
        # reset color and redraw
        self._color[0] = -1
        self.draw()
        time.sleep(self.p2)

    # utilities
    def get(self, i): return self._items[i]
    def size(self): return len(self._items)
    
    # due to the implementation of our top-down
    # propagation we must enforce a bounds check
    def compare(self, a, b):
        if b >= len(self._items): return True
        if a >= len(self._items): return False
        # color both nodes orange (ANSI 33)
        self._color = [a, b]
        self._highlight = "33"
        self.draw()
        # pause and reset highlights and redraw
        time.sleep(self.p1)
        self._color = [-1, -1]
        self.draw()
        time.sleep(self.p2)
        # return result of comparison
        return self._items[a] < self._items[b]

    # animated swap
    def swap(self, a, b):
        # color blue (ANSI 36)
        self._color = [a, b]
        self._highlight = "36"
        self.draw()
        # lazy swap
        t = self._items[a]
        self._items[a] = self._items[b]
        self._items[b] = t
        # render half-frame to animate transition
        # while still taking only `self.p1` seconds
        time.sleep(self.p1/2)
        self.draw()
        time.sleep(self.p1/2)
        # reset highlights and redraw
        self._color = [-1, -1]
        self.draw()
        time.sleep(self.p2)

    # pretty print tree - this method does the vast majority of the work!
    def draw(self):
        # because we are printing so much at a time, we don't want the
        # OS to fragment it into many lines, or it'll look flickery.
        # We print the entire tree as a single large string with newlines.
        out_str = ""
        # alignment is complicated!
        next_layer = 2
        spacing = 1
        tree_height = 1
        # offsets of top left corner of tree "bounding box"
        window_height = os.get_terminal_size()[1] - 1
        window_width = os.get_terminal_size()[0] // 2 + 1
        # log of 0 is undefined, so ignore when tree empty
        if len(self._items) > 1:
            spacing = int(math.pow(2, 1+int(math.log2(len(self._items)-1))))
            tree_height = 2*int(math.log2(len(self._items) - 1))
            window_width -= spacing
        window_height -= tree_height
        # when the tree is too big to fit in the terminal window, we get a ton of
        # garbage printouts, which we don't want. Instead print a nice dialog!
        if window_width < 0 or window_height < 0:
            # there is no tree; correct window offsets
            window_width += spacing
            window_height += tree_height
            out_str += '\n' * (window_height//2 - 2)
            s = "Your terminal is too small!"
            out_str += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            out_str += s + '\n'
            s = "Required: " + str(spacing + spacing + 1) + " x " + str(tree_height)
            out_str += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            out_str += s + '\n'
            s = "Current: " + str(os.get_terminal_size()[0]) + " x "
            s += str(os.get_terminal_size()[1])
            out_str += ' ' * ((os.get_terminal_size()[0] - len(s)) // 2)
            out_str += s + '\n'
            out_str += '\n' * (window_height - window_height//2 - 2)
            print(out_str)
            return
        # print top margin
        out_str += '\n' * (window_height - window_height//2)
        # left margin
        out_str += ' ' * window_width
        # loop over all values of tree and process
        for i in range(1, len(self._items)):
            # when we reach the next layer, we newline, and print out the dashes
            # representing edges of the tree
            if i == next_layer:
                # spacing cuts in half each layer
                spacing //= 2
                # layer indices are always powers of 2 (2, 4, 6, 8, etc)
                next_layer *= 2
                # newline and left margin
                out_str += '\n'
                out_str += ' ' * window_width
                # loop over elemnts of this layer
                for j in range(i, len(self._items)):
                    # of course we don't want to process elements that are outside
                    # of this layer; that would be unnecessary
                    if j == next_layer: break
                    # if both endpoints of the edge are colored, color the edge too.
                    # The math works out really nicely here!
                    if [j, j//2] == self._color or [j//2, j] == self._color:
                        out_str += "\033[0;" + self._highlight + 'm'
                    # not all gaps between indices have dashes - only even -> odd
                    # we only draw dashes on the correct side, and spaces on the other
                    out_str += (' ' if j%2 == 0 else '-') * (spacing-1)
                    out_str += ' '
                    out_str += ('-' if j%2 == 0 else ' ') * (spacing-1)
                    # correct for possible coloration
                    out_str += " \033[0m"
                # newline and left margin
                out_str += '\n'
                out_str += ' ' * window_width
            # print out actual nodes
            out_str += ' ' * (spacing-1)
            out_str += "\033[0;"
            if i in self._color:
                out_str += self._highlight
            else:
                out_str += "37"
            out_str += 'm'
            out_str += str(self._items[i])
            out_str += "\033[0m"
            out_str += ' ' * spacing
        # lower margin
        out_str += '\n' * (window_height//2)
        # finally print it all out
        print(out_str)
