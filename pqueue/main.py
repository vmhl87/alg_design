# Import necessary components to interface with heap
# - PauseTime for animations
# - Status for status text
# - Heap of course to make everything work!
from container import PauseTime, Status
from heap import Heap

# - State datastructure so we can use it
# - sort_on to change global sort metric
# - Stats to use metric listings, used to verify if metrics are valid
from state import State, sort_on
from regions import Regions
from stats import Stats

# - To use the slightly more organized help menu
from docs import Help

# - handle pauses
import time


# Simple wrapper to yes/no with simple ANSI coloring
def confirm(prompt):
    return input(prompt + " (y/\033[1mN\033[0m) ") in ["y", "yes", "Y", "Yes"]


# These are the main datastructures used in the course of the simulation -
# heap is used, of course, for the heap, and active is a set() used to ensure
# no element is inserted twice.
heap = Heap()
active = set()

# Tune animation speed
PauseTime(0.6, 0.2)


# Utilities to add single or groups of states, and update active set()
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


# Enter main loop!
print("Welcome! Run \033[1m`help`\033[0m to get started.")

while True:
    # Ask user for input and split into its component args
    i = input("\n> ").split()

    # If empty we can't index; i[0] would throw an error
    if len(i) == 0: continue

    # Handle exit behavior
    if i[0] in ["exit", "quit", "q"]:
        # handy confirmation dialog!
        if confirm("Are you \033[1msure\033[0m you want to exit?"):
            print("Exiting...")
            break
        else:
            print("Aborted")

    # Secret quick exit shortcut ;)  Not in help menus anywhere!
    elif i[0] == "qy":
        break

    # Display help information, and passthrough all additional args
    elif i[0] in ["help", "Help", "h", "H"]:
        Help(i[1:])

    # Pop off top item if the heap isn't empty
    elif i[0] in ["pop", "Pop", "p", "P"]:
        if heap.empty():
            print("Heap is empty - you cannot pop!")
        else:
            heap.pop()

    # Handle metrics
    elif i[0] in ["sort", "Sort", "s", "S"]:
        metric = ""

        # If a metric is given, process it:
        if len(i) > 1:
            # For style we allow the user to use "Sort on metric", handle here
            if i[1] == "on":
                # assuming a metric is given, use it
                if len(i) > 2:
                    metric = i[2]
                else:
                    # otherwise, error
                    print("Sort expected 1 argument, none given. " + 
                    "Consult \033[1m`help sort`\033[0m for more info.")
                    continue
            else:
                # if there is no "on", simply take the first argument as the metric
                metric = i[1]
        # if no metric given then error
        else:
            print("Sort expected 1 argument, none given. " + 
            "Consult \033[1m`help sort`\033[0m for more info.")
            continue

        # if the metric isn't actually a metric list out all the metrics
        if metric in ["list", "l"]:
            print("Valid sorting metrics:")
            for metric in Stats:
                print("    '" + metric + "'")

        # if it is an actual metric and it exists in Stats, we can use it without error.
        elif metric in Stats:
            sort_on(metric)
            print("Sorting on \033[1m" + metric + "\033[0m")
            time.sleep(0.5)
            # If the heap isn't empty we rebalance it. If the heap is empty we can skip.
            if not heap.empty():
                print("Rebalancing...")
                time.sleep(1)
                heap.rebalance()

        # error if invalid
        else:
            print("Invalid sort metric. Run \033[1m`sort list`\033[0m for a list " +
            "of sorting metrics, or \033[1m`help sort`\033[0m for usage instructions.")

    # Handle addition of states
    elif i[0] in ["add", "Add", "a", "A"]:
        # Error when insufficient args
        if len(i) == 1:
            print("Add expected 1 argument, none given. " +
            "Consult \033[1m`help add`\033[0m for more info.")
            continue
        
        # if we are instead querying for a list of regions do so
        if i[1] in ["list", "l"]:
            print("Valid regions:")
            for region in Regions:
                print("    '" + region + "'")

        # Little hack to see if the argument given is a state abbreviation - if it exists
        # in population information, it is a valid state
        elif i[1] in Stats["population"]:
            print("Adding \033[0;32m" + i[1] + "\033[0m...")
            time.sleep(1)
            add_state(i[1])

        # if it has commas, process all arguments as if multiple states
        elif len(i[1]) and i[1][-1] == ",":
            # list of states to append
            append = []

            for x in range(1, len(i)):
                # cut off commas
                i[x] = i[x].replace(",", "")

                # sometimes split() leaves empty strings
                if len(i[x]) == 0:
                    break

                # check if valid state
                if i[x] in Stats["population"]:
                    append.append(i[x])

                # otherwise, error
                else:
                    print("Invalid state/region. Run \033[1m`add list`\033[0m for a list " +
                    "of regions, or \033[1m`help add`\033[0m for usage instructions.")
                    append.append(False)
                    break

            # if all states valid then add all of them to heap
            # (note that if they are already in the heap then not all of them
            # will necessarily be appended)
            if len(append) and append[-1]:
                print("Adding states...")
                time.sleep(1)
                add_states(append)

        # otherwise if it is a region, append all states in said region
        elif i[1] in Regions:
            print("Adding \033[0;36m" + i[1] + "\033[0m...")
            time.sleep(1)
            add_states(Regions[i[1]])

        # otherwise error
        else:
            print("Invalid state/region. Run \033[1m`add list`\033[0m for a list " +
            "of regions, or \033[1m`help add`\033[0m for usage instructions.")

    # handle heap reset
    elif i[0] in ["reset", "Reset", "r", "R"]:
        # no need to reset an empty heap
        if heap.empty():
            print("Heap is already empty!")
            continue

        # nice confirmation dialog
        if confirm("Are you \033[1msure\033[0m you want to reset heap?"):
            print("Resetting...")
            time.sleep(1)
            Status("")
            heap = Heap()
            active = set()
        else:
            print("Aborted")

    # handle invalid
    else:
        print("Invalid command. Run \033[1m`help`\033[0m for instructions.")
