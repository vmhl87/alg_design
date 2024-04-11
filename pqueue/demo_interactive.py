from container import PauseTime
from heap import Heap
import random
import time
import math

mapping = ["1;30", "1;31", "1;32", "1;33", "1;34", "1;35"]
def rnc():
    return mapping[math.floor(random.random() * len(mapping))]

flip = False

class SwitchableInt:
    def __init__(self, i):
        self.i = i
        self.c = "\033[" + rnc() + 'm' + str(self.i) + "\033[0m"

    def __str__(self):
        return self.c

    def __lt__(self, o):
        return (self.i < o.i) ^ flip

collection = [SwitchableInt(i) for i in range(1, 10)]

random.shuffle(collection)

PauseTime(0.5, 0.1)

heap = Heap()

heap.fill(collection)

while True:
    choice = input("Sort direction? (up/down): ")
    if choice == "up":
        flip = False
    elif choice == "down":
        flip = True
    elif choice in ["exit", "quit", "e", "q"]:
        print("Exiting")
        break
    else:
        print("Invalid input")
        continue
    print("Rebalancing heap")
    time.sleep(0.8)
    heap.rebalance()
