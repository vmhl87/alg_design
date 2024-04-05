# import necessary components
# - PauseTime necessary to interact with rendering
# - Heap necessary for heapsort
# - random necessary for random input
# - sys necessary for command line args
from container import PauseTime
from heap import Heap
import random
import sys

# default values - 15 nodes, 0.8 second move, 0.2 second pause
nodes = 15
move_time = 1.5
pause_time = 0.3

# read system arguments and parse
if len(sys.argv) > 1:
    # assume first argument is node count, if it is not an int,
    # then print a usage dialog
    try:
        nodes = int(sys.argv[1])
    except:
        print("demo.py <node count> <move time> <pause time>")
        exit()
if len(sys.argv) > 2: move_time = float(sys.argv[2])
if len(sys.argv) > 3: pause_time = float(sys.argv[3])

PauseTime(move_time, pause_time)

# because Container() works best with single-char printable inputs,
# we mod to the digits 1-9
values = [1+i for i in range(0, nodes)]

# rearrange
random.shuffle(values)

#initialize heap
priority_queue = Heap()

# fill heap - this is animated
for i in values:
    priority_queue.push(i)

# drain heap - this is also animated
while not priority_queue.empty():
    priority_queue.pop()
