# string distance, bottom up dynamic

def string_distance(s1, s2):
    distances = [[0 for j in range(len(s1)+1)] for i in range(len(s2)+1)]

    for j in range(len(s1)+1):
        distances[0][j] = j

    for i in range(1, len(s2)+1):
        distances[i][0] = i

    for i in range(len(s2)):
        for j in range(len(s1)):
            distances[i+1][j+1] = min(
                    min(
                        distances[i+1][j]+1,
                        distances[i][j+1]+1
                    ),
                    distances[i][j]+(0 if s2[i]==s1[j] else 1)
                )

    return distances[-1][-1]
