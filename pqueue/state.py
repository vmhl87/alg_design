from stats import Stats

sort_metric = "population"

def sort_on(metric):
    global sort_metric
    sort_metric = metric

class State:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return self.state
    
    def __lt__(self, other):
        return Stats[sort_metric][self.state] > Stats[sort_metric][other.state]
