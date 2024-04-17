# preset prices array
prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


# input n; preface with ANSI bold for style
n = int(input("Enter length of the rod: \033[1m"))

# prepare DP array - stores (max profit, parent)
# we look at the decomposition as some sort of tree
dp = [(-1, -1) for _ in range(n+1)]
dp[0] = (0, -1)


""" old recursive implementation
# determine optimal profit for length i
def opt(i):
    global dp

    # if already maximally computed, return such
    if dp[i][0] > -1:
        return dp[i]

    # otherwise assume best is 0 and iterate
    best = (0, -1)

    # for every possible price, try it:
    for j in range(10):
        # of course sometimes this is impossible when
        # the rod is not long enough
        if i > j:
            # check the optimal configuration for the sub-rod
            check = opt(i-j-1)
            # update best
            if check[0] + prices[j] > best[0]:
                best = (check[0] + prices[j], i-j-1)

    # save to dp array and return
    dp[i] = best
    return best


# compute maximal profit for length n
best = opt(n)
"""


# new iterative implementation
# this runs much more efficiently due to the lack of branch predictions
# also, it is shorter and cleaner
for i in range(1, n+1):
    # loop over all possible removals
    for j in range(10):
        # if removal is possible, compare it to optimal
        if i > j:
            if dp[i-j-1][0] + prices[j] > dp[i][0]:
                dp[i] = (dp[i-j-1][0] + prices[j], i-j-1)

# find optimal configuration of length n
best = dp[n]


# pretty print output - first, print price
print("\033[0mOptimally, we can get \033[1m" + str(best[0]) +
"\033[0m dollar" + ("s" if best[0] > 1 else "") + "!")

# then, propagate backwards through children in graph to find
# which cuttings happen and how many - store counts here
lookup = [0 for _ in range(10)]
# iterate back through tree until reach root
i, j = n, best[1]
while j > -1:
    lookup[i-j-1] += 1
    i = j
    j = dp[j][1]
# pretty-print output
ret = "We divide into: "
for i in range(10):
    if lookup[i]:
        # cool ANSI bold/gray
        ret += ("\033[1m" +  str(i+1) + "\033[1;30mx" +
        str(lookup[i]) + "\033[0m, ")
# clip ending comma and space
if ret[-1] == " " and ret[-2] == ",":
    ret = ret[:-2]
print(ret)
