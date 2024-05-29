points = [
        [4, 21],
        [5, 19],
        [10, 24],
        [4, 17],
        [3, 16],
        [11, 25],
        [14, 24],
        [6, 22],
        [10, 21],
        [12, 21],
        [10, 5],
        [13, 11],
        [12, 7],
        [8, 9],
        [10, 10]
    ]

dim = [points[0][0], points[0][1], points[0][0], points[0][1]]

for point in points:
    for i in range(2):
        dim[i] = min(dim[i], point[i])
        dim[i+2] = max(dim[i+2], point[i])

for point in points: point.append(0)

class Centroid:
    def __init__(self, x, y):
        self.p = [x, y]
        self._p = [0, 0, 0]
        self.c, self._c = 0, 0

    def reset(self):
        self._p = [0, 0, 0]
        self._c, self.c = self.c, 0

    def cat(self, point):
        for i in range(2):
            self._p[i] += point[i]

        self._p[2] += 1

    def reap(self):
        if self._p[2] == 0:
            return False

        new = [self._p[0]/self._p[2], self._p[1]/self._p[2]]

        if new[0] == self.p[0] and new[1] == self.p[1]:
            return False
        
        self.p = [x for x in new]

        return True

import random
centroids = []
for i in range(3):
    centroids.append(Centroid(
            random.uniform(dim[0], dim[2]),
            random.uniform(dim[1], dim[3])
        ))

def distance(a, b):
    return sum([(a[i]-b.p[i])**2 for i in range(2)])

while True:
    for centroid in centroids:
        centroid.reset()

    for point in points:
        best, choice = distance(point, centroids[0]), 0

        for i in range(len(centroids)):
            new = distance(point, centroids[i])

            if new < best:
                best, choice = new, i

        centroids[choice].cat(point)
        point[2] = choice

    diff = False

    for centroid in centroids:
        if centroid.reap():
            diff = True

    if not diff: break

f = open(".out.txt", "w")

f.write(str(len(points)) + '\n')

for i in range(2): dim[i+2] -= dim[i]

for point in points:
    relative = [(point[i]-dim[i])/dim[i+2] for i in range(2)]

    for i in range(2): f.write(str(int(relative[i]*400)) + ' ')
    f.write(str(point[2]) + '\n')

f.write(str(len(centroids)) + '\n')

for j in range(len(centroids)):
    relative = [(centroids[j].p[i]-dim[i])/dim[i+2] for i in range(2)]

    for i in range(2): f.write(str(int(relative[i]*400)) + ' ')
    f.write(str(j) + '\n')

f.close()
