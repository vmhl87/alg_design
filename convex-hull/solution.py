import sys
import math


f = open(sys.argv[1])

[start, end] = [
        [float(i) for i in f.readline().split(',')] + [0, 0]
    for _ in range(2)]

points = []

for line in f:
    points.append([float(i) for i in line.split(',')] + [0, 0])

f.close()


points = [start] + sorted(points) + [end]


u, d = points[:1], points[:1]


us, ds = 0, 0
ul, dl = 1, 1


def slope(a, b):
    return (points[a][1]-points[b][1])/(points[a][0]-points[b][0])

for i in range(1, len(points)):
    p = points[i]
    while ul > 1 and slope(i, us) > slope(us, points[us][2]):
        us = points[us][2]
        ul -= 1
        u.pop()
    u.append(p)
    p[2] = us
    ul += 1
    us = i
    while dl > 1 and slope(i, ds) < slope(ds, points[ds][3]):
        ds = points[ds][3]
        dl -= 1
        d.pop()
    d.append(p)
    p[3] = ds
    ds = i
    dl += 1


print("\033[1;30m")
c = 0
for p in points:
    p.append(c)
    print(p)
    c += 1
print("--")
for p in u: print(p)
print("--")
for p in d: print(p)
print("--")
print(ul, dl)


p1, p2, loc = 0, 0, len(points) - 1

while loc > 0:
    ol = loc
    loc = points[loc][2]
    p1 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


loc = len(points) - 1

while loc > 0:
    ol = loc
    loc = points[loc][3]
    p2 += math.sqrt(
        (points[ol][0] - points[loc][0])**2 +
        (points[ol][1] - points[loc][1])**2
    )


print("--")
print(p1, p2)
print("--\033[0m")


ind = 2 if p1 < p2 else 3

print("Shortest distance is:", min(p1, p2))

loc = len(points) - 1

while loc > 0:
    print(str(points[loc][0]) + ',' + str(points[loc][1]))
    
    loc = points[loc][ind]

print(str(points[0][0]) + ',' + str(points[0][1]))
