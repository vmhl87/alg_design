a = open("movies_name.list")

f = open("movie_names/0.list", "w")
c = 0
i = 0

l = 38592396 # 13205098

for _ in range(l):
    p = a.readline()
    f.write(p)
    c += 1

    if c == 100000:
        i += 1
        f.close()
        f = open("movie_names/" + str(i) + ".list", "w")
        c = 0
        print("itr", i)

f.close()
