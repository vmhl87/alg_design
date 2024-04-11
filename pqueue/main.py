from container import PauseTime, Status
from heap import Heap

from state import State, sort_on
from regions import Regions
from stats import Stats

from docs import Help

import random
import time


def confirm(prompt):
    return input(prompt + " (y/\033[1mN\033[0m) ") in ["y", "yes", "Y", "Yes"]


heap = Heap()
active = set()

PauseTime(0.6, 0.2)


def add_state(state):
    if state not in active:
        active.add(state)
        heap.push(State(state))

def add_states(states):
    append = []

    for state in states:
        if state not in active:
            active.add(state)
            append.append(State(state))

    heap.push_list(append)


print("Welcome! Run \033[1m`help`\033[0m to get started.")

while True:
    i = input("\n> ").split()

    if len(i) == 0: continue

    if i[0] in ["exit", "quit", "q"]:
        if confirm("Are you \033[1msure\033[0m you want to exit?"):
            print("Exiting...")
            break
        else:
            print("Aborted")

    elif i[0] == "qy":
        break

    elif i[0] in ["help", "Help", "h", "H"]:
        Help(i[1:])

    elif i[0] in ["pop", "Pop", "p", "P"]:
        if heap.empty():
            print("Heap is empty - you cannot pop!")
        else:
            heap.pop()

    elif i[0] in ["sort", "Sort", "s", "S"]:
        metric = ""

        if len(i) > 1:
            if i[1] == "on":
                if len(i) > 2:
                    metric = i[2]
                else:
                    print("Sort expected 1 argument, none given. " + 
                    "Consult \033[1m`help sort`\033[0m for more info.")
                    continue
            else:
                metric = i[1]
        else:
            print("Sort expected 1 argument, none given. " + 
            "Consult \033[1m`help sort`\033[0m for more info.")
            continue

        if metric in ["list", "l"]:
            print("Valid sorting metrics:")
            for metric in Stats:
                print("    '" + metric + "'")
        elif metric in Stats:
            sort_on(metric)
            print("Sorting on \033[1m" + metric + "\033[0m")
            time.sleep(0.5)
            if not heap.empty():
                print("Rebalancing...")
                time.sleep(1)
                heap.rebalance()
        else:
            print("Invalid sort metric. Run \033[1m`sort list`\033[0m for a list " +
            "of sorting metrics, or \033[1m`help sort`\033[0m for usage instructions.")

    elif i[0] in ["add", "Add", "a", "A"]:
        if len(i) == 1:
            print("Add expected 1 argument, none given. " +
            "Consult \033[1m`help add`\033[0m for more info.")
            continue
        
        if i[1] in ["list", "l"]:
            print("Valid regions:")
            for region in Regions:
                print("    '" + region + "'")

        elif i[1] in Stats["population"]:
            print("Adding \033[0;32m" + i[1] + "\033[0m...")
            time.sleep(1)
            add_state(i[1])

        elif len(i[1]) and i[1][-1] == ",":
            append = []

            for x in range(1, len(i)):
                i[x] = i[x].replace(",", "")

                if len(i[x]) == 0:
                    break

                if i[x] in Stats["population"]:
                    append.append(i[x])
                else:
                    print("Invalid state/region. Run \033[1m`add list`\033[0m for a list " +
                    "of regions, or \033[1m`help add`\033[0m for usage instructions.")
                    append.append(False)
                    break

            if len(append) and append[-1]:
                print("Adding states...")
                time.sleep(1)
                add_states(append)

        elif i[1] in Regions:
            print("Adding \033[0;36m" + i[1] + "\033[0m...")
            time.sleep(1)
            add_states(Regions[i[1]])

        else:
            print("Invalid state/region. Run \033[1m`add list`\033[0m for a list " +
            "of regions, or \033[1m`help add`\033[0m for usage instructions.")

    elif i[0] in ["reset", "Reset", "r", "R"]:
        if heap.empty():
            print("Heap is already empty!")
            continue

        if confirm("Are you \033[1msure\033[0m you want to reset heap?"):
            print("Resetting...")
            time.sleep(1)
            Status("")
            heap = Heap()
            active = set()
        else:
            print("Aborted")

    else:
        print("Invalid command. Run \033[1m`help`\033[0m for instructions.")
