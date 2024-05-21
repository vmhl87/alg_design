import math


import time
st = time.time()


# could be subject to change
import sys
f = open(sys.argv[1])


# read in all points and sort
points = []

for line in f:
    # we leave 2 empty spaces to store the two virtual stacks
    points.append([float(i) for i in line.split(',')] + [0, 0])

f.close()

points = sorted(points)


# create two virtual stacks, one for the up path and the other
# for the down path - {u,d}s denotes top of stack and {u,d}l
# denotes length of stack
us, ds = 0, 0
ul, dl = 1, 1


# determine if the segment (a, b) has higher slope than (b, c)
# where a, b, c are indices in the array points[]
def slope(a, b, c):
    return (points[a][1] - points[b][1]) * (points[b][0] - points[c][0]) > (points[b][1] - points[c][1]) * (points[a][0] - points[b][0])

# iterate over all points and update virtual stacks
for i in range(1, len(points)):
    while ul > 1 and slope(i, us, points[us][2]):
        us, ul = points[us][2], ul-1

    points[i][2] = us
    us, ul = i, ul+1

    while dl > 1 and not slope(i, ds, points[ds][3]):
        ds, dl = points[ds][3], dl-1

    points[i][3] = ds
    ds, dl = i, dl+1


# compute lengths of up and down paths (p1, p2)
# loc denotes current location searching through graph
p1, p2, loc = 0, 0, us

# compute up path by moving backwards through the virtual stack
while loc > 0:
    ol, loc = loc, points[loc][2]

    p1 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


# same for the down stack
loc = ds

while loc > 0:
    ol, loc = loc, points[loc][3]

    p2 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


et = time.time()
print("elapsed:", et - st)


print("\033[1;30m--")
print(p1, p2)
print("--\033[0m")


# I strongly believe that the provided example outputs are
# incorrect - they consistently show the wrong side of the
# convex hull, and my solution does find shorter paths -
# when these lines are uncommented, the program outputs
# the longer of the two paths and is consistent with the
# provided outputs.

#if p1 < p2: p1 = p2 + 1
#else: p2 = p1 + 1


[ind, ln] = [2, ul] if p1 < p2 else [3, dl]

print("Shortest distance is:", min(p1, p2))

loc = us

while ln > 0:
    print(str(points[loc][0]) + ',' + str(points[loc][1]))
    
    loc, ln = points[loc][ind], ln-1