import math


# could be subject to change
import sys
f = open(sys.argv[1])


# read in all points and sort
points = []

for line in f:
    points.append([float(i) for i in line.split(',')] + [0, 0])

f.close()

points = sorted(points)


# u, d = points[:1], points[:1]


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
    p = points[i]
    while ul > 1 and slope(i, us, points[us][2]):
        us = points[us][2]
        ul -= 1
        # u.pop()
    # u.append(p)
    p[2] = us
    ul += 1
    us = i
    while dl > 1 and not slope(i, ds, points[ds][3]):
        ds = points[ds][3]
        dl -= 1
        # d.pop()
    # d.append(p)
    p[3] = ds
    ds = i
    dl += 1


# print("\033[1;30m")
# c = 0
# for p in points:
#     p.append(c)
#     print(p)
#     c += 1
# print("--")
# for p in u: print(p)
# print("--")
# for p in d: print(p)
# print("--")
# print(ul, dl)


# compute lengths of up and down paths (p1, p2)
# loc denotes current location searching through graph
p1, p2, loc = 0, 0, us

# compute up path by moving backwards through the virtual stack
while loc > 0:
    ol = loc
    loc = points[loc][2]
    p1 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


# same for the down stack
loc = ds

while loc > 0:
    ol = loc
    loc = points[loc][3]
    p2 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


# print("--")
# print(p1, p2)
# print("--\033[0m")


ind = 2 if p1 < p2 else 3

print("Shortest distance is:", min(p1, p2))

loc = us

while loc > 0:
    print(str(points[loc][0]) + ',' + str(points[loc][1]))
    
    loc = points[loc][ind]

print(str(points[0][0]) + ',' + str(points[0][1]))
