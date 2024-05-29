# hardcoded point values
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


# compute upper and lower bounds on x, y
dim = [points[0][0], points[0][1], points[0][0], points[0][1]]

for point in points:
    for i in range(2):
        dim[i] = min(dim[i], point[i])
        dim[i+2] = max(dim[i+2], point[i])


# store color in points array
for point in points: point.append(0)


# centroid datastructure, manages everything internally
class Centroid:
    def __init__(self, x, y):
        # current position
        self.p = [x, y]
        # aggregated position from sub-points and count
        # (pre-average)
        self._p = [0, 0, 0]
        # child counts
        self.c, self._c = 0, 0

    # reset for new iteration - clear preaverage and rotate counts
    def reset(self):
        self._p = [0, 0, 0]
        self._c, self.c = self.c, 0

    # concatenate a point to self - aggregate position
    def cat(self, point):
        for i in range(2):
            self._p[i] += point[i]

        self._p[2] += 1

    # average out and return if changes occured
    def reap(self):
        if self._p[2] == 0:
            return False

        new = [self._p[0]/self._p[2], self._p[1]/self._p[2]]

        if new[0] == self.p[0] and new[1] == self.p[1]:
            return False
        
        self.p = [x for x in new]

        return True


# randomly seed initial centroids
import random
centroids = []
for i in range(3):
    centroids.append(Centroid(
            random.uniform(dim[0], dim[2]),
            random.uniform(dim[1], dim[3])
        ))


# helper for distance squared
def distance(a, b):
    return sum([(a[i]-b.p[i])**2 for i in range(2)])


# main loop - repeat until break
while True:
    # reset all centroids
    for centroid in centroids:
        centroid.reset()

    # for each point, compute closest centroid
    for point in points:
        best, choice = distance(point, centroids[0]), 0

        for i in range(1, len(centroids)):
            new = distance(point, centroids[i])

            if new < best:
                best, choice = new, i

        # update both color of point and centroid aggr
        centroids[choice].cat(point)
        point[2] = choice

    # check if differences
    diff = False

    for centroid in centroids:
        if centroid.reap():
            diff = True

    # if nothing changed, end loop
    if not diff: break


# write out results
f = open(".out.txt", "w")

f.write(str(len(points)) + '\n')

# renormalize bounds to [x, y, w, h]
for i in range(2): dim[i+2] -= dim[i]

# write out point coordinates normalized to 400x400 square
for point in points:
    relative = [(point[i]-dim[i])/dim[i+2] for i in range(2)]

    for i in range(2): f.write(str(int(relative[i]*400)) + ' ')
    f.write(str(point[2]) + '\n')

f.write(str(len(centroids)) + '\n')

# repeat for centroids
for j in range(len(centroids)):
    relative = [(centroids[j].p[i]-dim[i])/dim[i+2] for i in range(2)]

    for i in range(2): f.write(str(int(relative[i]*400)) + ' ')
    f.write(str(j) + '\n')

# close file stream
f.close()
