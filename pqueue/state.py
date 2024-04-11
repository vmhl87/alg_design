# Import stats to use for sorting
from stats import Stats

# Keep a global variable for the sorting metric, which can be edited
# by an external method.
sort_metric = "population"

def sort_on(metric):
    global sort_metric
    sort_metric = metric

# Extremely simplistic wrapper that supports comparison and printing
class State:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return self.state
    
    # Because we want highest value at the top, we do sort in reverse
    def __lt__(self, other):
        return Stats[sort_metric][self.state] > Stats[sort_metric][other.state]
