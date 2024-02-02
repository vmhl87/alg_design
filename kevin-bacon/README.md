### Overview

Hello! This is a short overview of how my program(s) work. The code isn't very stylistically convoluted, (for once), but it might be unclear exactly how it is working.

### The Kevin Bacon Problem

IMDB publishes a database of actors and films. It hosts this data online in the form of several gzipped .tsv (tab separated value) files. There are several files, but I only
found three necessary - `name.basics.tsv`, `title.akas.tsv`, and `title.principals.tsv`.

`name.basics.tsv` contains the names and alphanumeric identifiers of all of the actors. Alphanumerics are unique to each actor.

`title.akas.tsv` contains the titles, alphanumerics, and regions of all of the films. For sake of simplicity, I only parsed films
with region `US` or `EN`.

`title.principals.tsv` contains the roles that actors played in films. Each row in this file contains an alphanumeric identifier of an actor,
an alphanumeric identifier of the film they were in, and their role.

### Building a graph

First, my program needed to collect all of this data and format it into a graph-like structure. From the data given, it was clear how I could easily do this:

Graphs have nodes and edges. The nodes in my graph are the actors *and* the movies. The nodes are the actor's roles - if an actor plays some role in a movie,
they are connected to that movie by an edge.

This looks like it complicates the graph somewhat, but it really doesn't Actors are only connected to movies, and movies are only connected to actors.
Graph traversal doesn't care what type of node is what, as long as it can find a path from one vertex to another.

### Implementation

Alphanumerics are great for uniquely identifying objects in large datasets, but they aren't very program-friendly. I built a system to convert easily between
integer index and alphanumeric identifier:

index -> alphanumeric conversion was very easy; I simply made four arrays of strings

```c++
string *movies_apn = new string[akas_len];
string *movies_name = new string[akas_len];
string *actors_apn = new string[name_len];
string *actors_name = new string[name_len];
```

Note the `*` - these arrays are allocated on the heap, because they are so large, and their associated variables are actually pointers to their location in memory.
This is important when we delete them later, because c++ doesn't have built-in garbage collection, and I don't like using external libraries.

alphanumeric -> index conversion was a bit more complex; however, I could simply use a hashmap.

```c++
map<string, int> actor_index;
map<string, int> movie_index;
```

Because `map<T>` is an abstract datatype, it is automatically allocated on the heap, by virtue of its allocation function, and it has a built-in deallocation function
that watches for when its stack-facing variable is deleted, and automatically clears the memory for us.

These essentially behave like arrays in terms of how we access them.

Reading in data from the huge text files was a bit tedious - c++ doesn't have as complex string parsing as Python does.

I parsed the strings manually, character by character. I've done this a lot before, so it wasn't that bad.

```c++
for(long long i=0;i<name_len;i++){
  // read entire line onto string
  string s; getline(names, s);
  //  sw (swap) stores whether or not we have    \
      reached the separating tab and are reading \
      name rather than apn
  bool sw=0;
  // loop over all characters
  for(char c:s){
    // if we encounter a tab character:
    if(c=='	'){
      //  if we've already swapped once, we are done \
          and break out of the loop
      if(sw) break;
      // otherwise, swap and continue
      sw = 1; continue;
    }
    // append character to correct string
    if(sw) actors_name[i] += c;
    else actors_apn[i] += c;
  }
  // update hashmap
  actor_index[actors_apn[i]] = i;
}
```

A similar structure was used to parse the other files.

Now that I had the alphanumeric identifiers and names neatly filed away and associated with indices, I could print them into their own files to make
future access to these values not as complex.

I then deleted the arrays associated with name and alphanumeric identifier, since I didn't need them anymore, and they took up almost a gigabyte.

I had to delete them manually, as they were heap arrays.

```c++
delete[] movies_apn;
delete[] movies_name;
// etc.
```

I did not delete the hashmaps, because I needed them for the second part - parsing the edge data, and compiling it into a series of adjacency lists.

To store adjacency lists, I created a pair of sets.

```c++
unordered_set<int> *actor_adj = new unordered_set<int>[name_len];
unordered_set<int> *movie_adj = new unordered_set<int>[akas_len];
```

I then used a similar character-by-character parse to fill in the adjacencies. I then wrote them out to their own files, and the parsing was complete.

The files being parsed here are huge! In total, they take up several gigabytes, and their line counts are in the tens of millions.

Well, now that I had the parsed data in a convenient format, I could write the second part of this program - the traversal algorithm.

### Traversing a bistate graph

I had to build a datastructure that could store the graph information in a way that could be accessed efficiently, and also be space-efficient.

To do this, I made two seperate types of nodes - one to populate the adjacency lists, and the other to be used during traversal, where less
information needed to be stored, but it had to be allocated and deallocated far faster.

```c++
typedef struct{
	int id;
	int n_adj;
	int *adj; // array stored on the heap
	bool init = 0;
} node;

typedef struct{
	int id; // points to a `node` - doesn't actually store the entire adjlist
	int depth;
	int from;
	bool is_act = 1;
} traverse_node;
```

The trick here is that I created a static `node` array, which stored their adjlists internally, and stored *which node to access* inside each of the traversal
nodes. This had the benefit of both extremely fast access time to adjlists, but also extremely fast allocation of traversal nodes.

Each `node` contains an internal heap array that needs to be manually allocated at runtime. Allocation of thee `node` array was a bit tedious, but it worked well.

```c++
node *act_adjlist = new node[name_len];

// ...a bunch of code in between...

for(int i=0;i<name_len;i++){
  // ... other code ...
  act_adjlist[i].adj = new int[n_adjacent];
  // ... other code ...
}
```

Once all the datastructures were loaded, traversing was very simple. I wrote a `search()` function which prompted the user for an input, and traversed from there to Kevin Bacon.
If the user entered "exit", the program would stop, otherwise, it would prompt the user for a new input.

Additionally, it would display a tip the first time it was run, but no more once it was rerun. This was represented by a boolean argument `first`.

```c++
if(first) cout << "Enter the name of an actor, or 'exit' to exit:\n";
cout << "> ";
string actor; getline(cin, actor);

if(actor == "exit") return;
```

Note that c++ requires explicit printing of newlines, unlike python. I quite like this, actually.

Using the collected list of names, the program could efficiently locate the index of the actor in question, if they existed:

```c++
int actor_id = -1;

for(int i=0;i<name_len;i++){
  if(actor_namelist[i] == actor){
    actor_id = i;
    break;
  }
  progress(i*100/name_len);
}
```

The `progress()` function here is a little utility I wrote which draws a progress bar at the bottom of the terminal.

The program then handled invalid input.

```c++
if(actor_id+1)
  cout << "\nFound " << actor << " at index " << actor_id << '\n';
else{
  cout << "\nCouldn't find " << actor << " in namelist\n\n";
  search(0);
  return;
}
```

Next was the traversal. Initially I tried to use DFS, as its traversal stack would contain the entire path of nodes traversed
to get to the target, but its non-direct nature was prohibitive. I had to use BFS, and figure out how to backtrack.

I did this in a somewhat unorthodox way - rather than using an actual queue, I used a variable length array (vector) and kept track of
a "virtual start position", which was advanced in order to "pop objects off" of the queue.

```c++
vector<traverse_node> search_queue;
int front_index = 0;
```

I implemented backtracking in the datastructure itself. Recall that the `traverse_node` structure is as follows:

```c++
typedef struct{
	int id;
	int depth;
	int from; //   <-- actually just an index to whatever node it came from
	bool is_act = 1;
} traverse_node;
```

It's a somewhat hacky solution, but works, and avoids allocating a massive array. (i.e. edgeTo)

We also don't want our search queue to backtrack upon itself. I used a set for this.

```c++
unordered_set<int> actors_visited;
unordered_set<int> movies_visited;
```

To initialize these datastructures, I pushed the inputted actor onto the queue, and updated the `actors_visited` set.

```c++
search_queue.push_back(actor_node_at(actor_id));
actors_visited.insert(actor_id);
```

`actor_node_at()` is a helper function that generates a `traverse_node` from an index, as c++ structs do not have constructors.

The traversal was accomplished with a while loop. It has a lot going on, so I'll break it down into pseudocode.

```c++
while(we are not finished) {
  update front node;

  if(front node is an actor node) {
    for(all movie nodes adjacent to front node) {
      if(movie node isn't visited yet) {
        set movie node as visited;
        append movie node to queue;
      }
    }
  } else {
    for(all actor nodes adjacent to front node) {
      if(actor node isn't visited yet) {
        set actor node as visited;
        append actor node to queue;
        if(actor node is Kevin Bacon) break out of all loops;
      }
    }
  }

  display progress;
}
```

Then, we use `traverse_node.from` to backtrace through the queue, and find our path, and print it.

Not only do we see which actor is connected to which, but through which movie!

This is a somewhat simplified explanation. Feel free to read the source code of both my c++ and Python implementations. (The Python implementation is not commented, but is
essentially the same code, minus the progress bars, because those did not work well with Python input/output streams.)

### Compiling

If you want to run this yourself, an IDE like VSCode might work. Alternatively, a command-line compiler like `g++` or `clang++` will work.

```
$ g++ parse.cpp -o ./parse.out
$ ./parse.out
<-- program output -->
$ g++ traverse.cpp -o ./traverse.out
$ ./traverse.cpp
<-- program output -->
```

I'm on a Linux system with the GNU c++ compiler (g++) installed, so compilation may be different for you.

### A note on time

Even my reasonably well optimized c++ parsing script takes over 4 minutes to run on my desktop, and it's a pretty powerful machine. The data involved is simply so large
and needs to be interconnected to a very high degree that there is no way to avoid direct computation of everything.

This is also where low-level languages are very useful. Python is a very easygoing language, with loose syntax. While this is good for some applications, it is less clear
exactly what operations are running under the hood - for example, what is actually happening in the loop `for i in range(10):`?

c++ would generally use something similar to `for(int i=0; i<10; i++){}`, which is much more direct and clear. Even iterator-based loops are more clear in c++.
