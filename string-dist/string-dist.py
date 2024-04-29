# string distance, bottom up dynamic

def string_distance(s1, s2, verbose=False):
    # create 2d state array - zeroed out
    distances = [[0 for j in range(len(s1)+1)] for i in range(len(s2)+1)]

    # fill first row and first column - these correspond to comparing
    # one prefix to the other empty prefix, and will be equal to the
    # length of the nonzero prefix
    for j in range(len(s1)+1):
        distances[0][j] = j
    for i in range(1, len(s2)+1):
        distances[i][0] = i

    # iterate over all other cells and set value
    for i in range(len(s2)):
        for j in range(len(s1)):
            # min of up+1, left+1, diagonal+cost
            distances[i+1][j+1] = min([
                    distances[i+1][j]+1,
                    distances[i][j+1]+1,
                    distances[i][j]+(0 if s2[i]==s1[j] else 1)
                ])

    # verbose printout
    if verbose:
        for row in distances:
            print(' '.join([str(i) for i in row]))

    # return bottom right cell corresponding to full word vs full word
    return distances[-1][-1]
