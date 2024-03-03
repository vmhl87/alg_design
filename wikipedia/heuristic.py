import random
import cohere
from cohere.responses.classify import Example


# drop-in for proper API key handling
def unscramble(x):
    return ''.join([chr(int(i)) for i in x.split()])

API_KEY = open('key.txt', 'r').read()
API_KEY = unscramble(API_KEY)


co = cohere.Client(API_KEY)


# graph routing stub - replace with proper code to
# traverse wikipedia and find adjacencies
from graph_route_stub import adj

class PageDistance:
    def __init__(self, root, depth=5, order_size=7):
        self.root = root
        self.order_size = order_size
        
        # the only zeroth order page is the root
        self.orders = [[root]]
        
        for i in range(depth):
            self.compute_next_order()

        # cohere won't be able to classify pages with only one
        # example, so we leave out root. We also don't need a heuristic
        # to be able to determine if we are at the root level.
        self.orders = self.orders[1:]
        
        # pre-process into "Example" datastructures to make
        # API calls easier
        for i in range(len(self.orders)):
            for j in range(len(self.orders[i])):
                # we add 1 to i - because we cut off the root from our orders
                # list, the zeroth element of our array is order 1, and the
                # first element in the array is order 2, etc.
                self.orders[i][j] = Example(self.orders[i][j], str(i+1))

        # concatenate into one large array
        self.orders = [page for order in self.orders for page in order]
    
    
    def compute_next_order(self):
        new_pages = []
        
        # extend from previous order
        for page in self.orders[-1]:
            # this is where we would use the real graph
            # traversal code
            for neighbor in adj(page):
                # we don't want to loop back on ourselves
                # while collecting orders
                is_new_page = True
                
                for order in self.orders:
                    for other_page in order:
                        if other_page == neighbor:
                            is_new_page = False
                            break
                    
                    if not is_new_page:
                        break
                
                if is_new_page:
                    new_pages.append(neighbor)

            # we only need to generate order_size new pages
            if len(new_pages) >= self.order_size:
                break

        # we can clip the previous order now that we have used it
        if len(self.orders[-1]) > self.order_size:
            random.shuffle(self.orders[-1])
            self.orders[-1] = self.orders[-1][:self.order_size]
        
        self.orders.append(new_pages)
    
    
    def distances(self, pages):
        response = co.classify(
            inputs=pages,
            examples=self.orders
        )

        distances = []

        for classification in response.classifications:
            average, total = 0, 0

            for order in classification.labels:
                confidence = classification.labels[order].confidence

                total += confidence
                average += confidence * int(order)

            average /= total

            # should 'distances' return only the computed heuristic or
            # a dict containing both distance and page label? not sure
            distances.append({'page': classification.input, 'distance': average})

        return distances
