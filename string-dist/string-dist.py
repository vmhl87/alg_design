# string distance, bottom up dynamic

def string_distance(s1, s2):
    s1, s2 = '_' + s1, '_' + s2

    distances = [[0 for j in range(len(s1))] for i in range(len(s2))]

    for j in range(len(s1)):
        distances[0][j] = j + (0 if s1[0]==s2[0] else 1)

    for i in range(1, len(s2)):
        distances[i][0] = i + (0 if s1[0]==s2[0] else 1)

    for i in range(1, len(s2)):
        for j in range(1, len(s1)):
            distances[i][j] = min(
                    min(
                        distances[i-1][j]+1,
                        distances[i][j-1]+1
                    ),
                    distances[i-1][j-1]+(0 if s2[i]==s1[j] else 1)
                )

    return distances[-1][-1]
