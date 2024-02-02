//  This is also written in c++ because of the size of the data involved. \
	Without any optimization or parallelization of input files, they take \
	up over 5GB of RAM. In Python they would undoubtedly take up more.    \
	This is an issue on my laptop, as it has only 4GB of RAM and 7GB of swap.

// imports
#include <unordered_set>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stack>
using namespace std;

//  datastructure to hold a node in adjacency list - it stores an integer \
	index, number of adjacent vertices, and an array of adjacent node     \
	indexes (stored as a heap array)
typedef struct{
	int id;
	int n_adj;
	int *adj;
	bool init = 0;
} node;

//  datastructure to hold node in traversal (holds depth, index, and which \
	node it branched from
typedef struct{
	int id;
	int depth;
	int from;
	bool is_act = 1;
} traverse_node;

// utility to draw progress bars
long long prc=100;
void progress(long long p) {
	if(p==100||p>prc||(p==0&&prc>0)) prc = p;
	else return;
	cout << "\r[";
	for(long long i=0;i<100;i+=2){
		if(i<p-1) cout << '=';
		else if(i==p-1) cout << '-';
		else cout << ' ';
	}
	cout << "] (" << p << "%)  ";
	fflush(stdout);
	if(p>=100) cout << '\n';
}

// global variables
const long long name_len = 13205098,
	            akas_len = 38592396;

// an, vn - {actor, movie} namelist pointers
string *an, *vn;
// al, vl - {actor, movie} adjacency list pointers
node *al, *vl;

// utility to create new nodes in traversal tree
traverse_node actor_node_at(int id, int depth, int from) {
	traverse_node tmp;
	tmp.id = id;
	tmp.depth = depth;
	tmp.from = from;
	return tmp;
}

traverse_node movie_node_at(int id, int depth, int from) {
	traverse_node tmp;
	tmp.id = id;
	tmp.is_act = 0;
	tmp.depth = depth;
	tmp.from = from;
	return tmp;
}

// overloads
traverse_node actor_node_at(int id) {
	return actor_node_at(id, 0, -1);
}

traverse_node movie_node_at(int id) {
	return movie_node_at(id, 0, -1);
}

// asks user for actor name until "exit" is entered
void search(bool first) {
	// ask for input, and display tip on first run
	if(first) cout << "Enter the name of an actor, or 'exit' to exit:\n";
	cout << "> ";
	string actor; getline(cin, actor);
	
	// exit if exit is entered
	if(actor == "exit") return;
	
	// find actor in actor namelist
	cout << "Searching for " << actor << " in namelist\n";
	
	int actor_id = -1;
	
	for(int i=0;i<name_len;i++){
		if(an[i] == actor){
			actor_id = i;
			break;
		}
		progress(i*100/name_len);
	}
	
	//  actor_id is by default -1, so if it is still -1, we have not found \
		the actor, so we exit this run of the method
	if(actor_id+1)
		cout << "\nFound " << actor << " at index " << actor_id << '\n';
	else{
		cout << "\nCouldn't find " << actor << " in namelist\n\n";
		search(0);
		// avoid complications
		return;
	}
	
	//  I wasn't able to use DFS due to the extreme size of the graph, \
		so BFS was necessary
	cout << "Building search queue\n";
	
	//  We actually want to keep every node that ever has entered the queue, \
		in order to backtrace to see what path we took (DFS doesn't have     \
		this issue, but a shortest path was necessary. I used a vector.
	vector<traverse_node> search_queue;
	int front_index = 0;
	
	// avoid repeating paths already traversed
	unordered_set<int> actors_visited;
	unordered_set<int> movies_visited;
	
	// initialize queue
	search_queue.push_back(actor_node_at(actor_id));
	actors_visited.insert(actor_id);
	
	cout << "Moving through graph\n";
	
	// keep track of "front node"
	int iter = 0, depth = 0;
	traverse_node front = search_queue[0];
	
	// we haven't found him yet!
	bool found_kevin_bacon = 0;
	// well, unless we started with him..
	if(actor == "Kevin Bacon") found_kevin_bacon = 1;
	
	// index of Kevin Bacon is 101
	while(!found_kevin_bacon && front_index < search_queue.size()){
		// update front node
		front = search_queue[front_index];
		front_index++;
		
		/*
		cout << front.id << " | ";
		if(front.is_act) cout << an[front.id];
		else cout << vn[front.id];
		cout << "\n\n";
		*/
		
		bool finished = 0;
		
		// bistate graph - nodes alternate between actor and movie
		if(front.is_act){
			// loop through all adjacent and append to queue
			if(al[front.id].init) for(int i=0;i<al[front.id].n_adj;i++){
				if(movies_visited.find(al[front.id].adj[i])
				!=movies_visited.end()) continue;
				movies_visited.insert(al[front.id].adj[i]);
				search_queue.push_back(
					movie_node_at(
						al[front.id].adj[i], front.depth+1, iter
					)
				);
			}
		}else{
			if(vl[front.id].init) for(int i=0;i<vl[front.id].n_adj;i++){
				if(actors_visited.find(vl[front.id].adj[i])
				!=actors_visited.end()) continue;
				actors_visited.insert(vl[front.id].adj[i]);
				search_queue.push_back(
					actor_node_at(
						vl[front.id].adj[i], front.depth+1, iter
					)
				);
				// found him!
				if(vl[front.id].adj[i] == 101){
					front = search_queue[search_queue.size()-1];
					found_kevin_bacon = 1;
					finished = 1;
					break;
				}
			}
		}

		if(finished) break;
		
		depth = front.depth;
		
		// update depth
		if(iter%13==0){
			cout << "\rDepth " << front.depth << " (" << iter << " iterations)";
			fflush(stdout);
		}
		
		iter++;
	}
	
	if(!found_kevin_bacon){
		cout << "\nCouldn't find a path from " << actor
			 << " to Kevin Bacon.\n\n";
		
		// rerun program
		search(0);
		return;
	}
	
	cout << "\nFound Kevin Bacon!\n";
	
	// because we need to backtrace, we use a stack
	stack<traverse_node> path;
	
	//  while front is not the root node (from -1), backtrace to its \
		root node
	while(front.from+1 && depth--> -3){
		path.push(front);
		
		front = search_queue[front.from];
	}
	
	if(depth < -2) cout << "An error might have occured.\n";
	
	// print out the path
	cout << "Path:\n";
	
	cout << actor;
	
	// print everything inside stack
	while(!path.empty()){
		traverse_node node = path.top();
		path.pop();
		
		if(node.is_act){
			// get name from namelist and print
			cout << an[node.id];
			if(node.id == 101) break;
		}else{
			cout << " --- (" << vn[node.id] <<  ") --> ";
		}
	}
	
	cout << "\n\n";
	
	// rerun
	search(0);
}

int main() {
	// initialze file streams
	cout << "Opening file streams\n";

	ifstream act_name("actors_name.list");
	ifstream act_adj("actors_adj.list");
	ifstream mov_name("movies_name.list");
	ifstream mov_adj("movies_adj.list");
	
	progress(100);
	
	// create arrays to store {actor, movie} name, adjlist
	cout << "Creating datastructures\n";
	
	progress(0);
	
	string *act_namelist = new string[name_len];
	
	// update global pointers
	an = act_namelist;
	
	node *act_adjlist = new node[name_len];
	
	// fill node ids
	for(int i=0;i<name_len;i++){
		act_adjlist[i].id = i;
		progress(i*100/(name_len+akas_len));
	}
	
	al = act_adjlist;
	
	string *mov_namelist = new string[akas_len];
	
	vn = mov_namelist;
	
	node *mov_adjlist = new node[akas_len];
	
	for(int i=0;i<akas_len;i++){
		mov_adjlist[i].id = i;
		progress((name_len+i+1)*100/(name_len+akas_len));
	}
	
	vl = mov_adjlist;
	
	// now we need to read from the files and process into our arrays
	cout << "Building adjacency lists\n";
	
	for(int i=0;i<name_len;i++){
		//  our adjacency lists contain the number of adjacent vertices \
			and then all of the vertices; we must then read in all of them
		int n_adjacent; act_adj >> n_adjacent;
		// update properties of object
		act_adjlist[i].n_adj = n_adjacent;
		// initialize heap array
		act_adjlist[i].adj = new int[n_adjacent];
		for(int j=0;j<n_adjacent;j++){
			act_adj >> act_adjlist[i].adj[j];
		}
		act_adjlist[i].init = 1;
		progress(i*100/(name_len+akas_len));
	}
	
	for(int i=0;i<akas_len;i++){
		int n_adjacent; mov_adj >> n_adjacent;
		mov_adjlist[i].n_adj = n_adjacent;
		mov_adjlist[i].adj = new int[n_adjacent];
		for(int j=0;j<n_adjacent;j++){
			mov_adj >> mov_adjlist[i].adj[j];
		}
		mov_adjlist[i].init = 1;
		progress((i+name_len+1)*100/(name_len+akas_len));
	}
	
	cout << "Reading names\n";
	
	for(int i=0;i<name_len;i++){
		getline(act_name, act_namelist[i]);
		progress(i*100/(name_len+akas_len));
	}
	
	for(int i=0;i<akas_len;i++){
		getline(mov_name, mov_namelist[i]);
		progress((i+name_len+1)*100/(name_len+akas_len));
	}
	
	cout << "Closing file streams\n";
	
	act_adj.close();
	act_name.close();
	mov_adj.close();
	mov_name.close();
	
	progress(100);
	
	cout << "Ready\n";
	
	// this is the first iteration so we run with first = true
	search(1);
	
	// clean up arrays
	cout << "Deleting datastructures\n";
	
	progress(0);
	
	delete[] act_namelist;
	
	progress(25);
	
	//  because each node has a heap array attached, we must explicitly \
		delete it, and then delete the outer array
	for(int i=0;i<name_len;i++){
		delete[] act_adjlist[i].adj;
		progress(25+i*25/name_len);
	}
	
	delete[] act_adjlist;
	
	progress(50);
	
	delete[] mov_namelist;
	
	progress(75);
	
	for(int i=0;i<akas_len;i++){
		delete[] mov_adjlist[i].adj;
		progress(75+i*25/akas_len);
	}
	
	delete[] mov_adjlist;
	
	progress(100);
	
	cout << "Exiting\n";
}
