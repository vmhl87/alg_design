#include <unordered_set>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stack>
using namespace std;

typedef struct{
	int id;
	int n_adj;
	int *adj;
} node;

typedef struct{
	int id;
	int depth;
	int from;
	bool is_act = 1;
} traverse_node;

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

const long long name_len = 13205098,
	            akas_len = 38592396;

string *an, *vn;
node *al, *vl;

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

void search(bool first) {
	if(first) cout << "Enter the name of an actor, or 'exit' to exit:\n";
	cout << "> ";
	string actor; getline(cin, actor);
	
	if(actor == "exit") return;
	
	cout << "Searching for " << actor << " in namelist\n";
	
	int actor_id = -1;
	
	for(int i=0;i<name_len;i++){
		if(an[i] == actor){
			actor_id = i;
			break;
		}
		progress(i*100/name_len);
	}
	
	if(actor_id+1)
		cout << "\nFound " << actor << " at index " << actor_id << '\n';
	else{
		cout << "\nCouldn't find " << actor << " in namelist\n\n";
		search(0);
	}
	
	cout << "Building search queue\n";
	
	vector<traverse_node> search_queue;
	int front_index = 0;
	
	unordered_set<int> actors_visited;
	unordered_set<int> movies_visited;
	
	search_queue.push_back(actor_node_at(actor_id));
	actors_visited.insert(actor_id);
	
	cout << "Moving through graph\n";
	
	int iter = 0;
	traverse_node front = search_queue[0];
	
	// index of Kevin Bacon is 101
	while(!front.is_act || front.id != 101){
		front = search_queue[front_index];
		front_index++;
		
		if(front.is_act){
			for(int i=0;i<al[front.id].n_adj;i++){
				//if(movies_visited.find(al[front.id].adj[i]) \
				!=movies_visited.end()) continue;             \
				movies_visited.insert(al[front.id].adj[i]);
				search_queue.push_back(
					movie_node_at(al[front.id].adj[i], front.depth+1, iter)
				);
			}
		}else{
			for(int i=0;i<vl[front.id].n_adj;i++){
				//if(actors_visited.find(vl[front.id].adj[i]) \
				!=actors_visited.end()) continue;             \
				actors_visited.insert(vl[front.id].adj[i]);
				search_queue.push_back(
					actor_node_at(vl[front.id].adj[i], front.depth+1, iter)
				);
			}
		}
		
		cout << "\rDepth " << front.depth << " (" << iter << " iterations)";
		fflush(stdout);
		
		iter++;
	}
	
	cout << "\nFound Kevin Bacon!\n";
	
	stack<traverse_node> path;
	
	// while curr.from is not -1 (root)
	while(front.from+1){
		path.push(front);
		
		front = search_queue[front.from];
	}
	
	cout << "Path:\n";
	
	cout << actor;
	
	while(!path.empty()){
		traverse_node node = path.top();
		path.pop();
		
		if(node.is_act){
			cout << " --> ";
			cout << an[node.id];
			if(node.id == 101) break;
		}else{
			//cout << " --- (" << vn[node.id] <<  ") --> ";
		}
	}
	
	cout << "\n\n";
	
	search(0);
}

int main() {
	cout << "Opening file streams\n";

	ifstream act_name("actors_name.list");
	ifstream act_adj("actors_adj.list");
	ifstream mov_name("movies_name.list");
	ifstream mov_adj("movies_adj.list");
	
	progress(100);
	
	cout << "Creating datastructures\n";
	
	progress(0);
	
	string *act_namelist = new string[name_len];
	
	an = act_namelist;
	
	node *act_adjlist = new node[name_len];
	
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
	
	cout << "Building adjacency lists\n";
	
	for(int i=0;i<name_len;i++){
		int n_adjacent; act_adj >> n_adjacent;
		act_adjlist[i].n_adj = n_adjacent;
		act_adjlist[i].adj = new int[n_adjacent];
		for(int j=0;j<n_adjacent;j++){
			act_adj >> act_adjlist[i].adj[j];
		}
		progress(i*100/(name_len+akas_len));
	}
	
	for(int i=0;i<akas_len;i++){
		int n_adjacent; mov_adj >> n_adjacent;
		mov_adjlist[i].n_adj = n_adjacent;
		mov_adjlist[i].adj = new int[n_adjacent];
		for(int j=0;j<n_adjacent;j++){
			mov_adj >> mov_adjlist[i].adj[j];
		}
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
	
	search(1);
	
	cout << "Deleting datastrucutres\n";
	
	progress(0);
	
	delete[] act_namelist;
	
	progress(25);
	
	for(int i=0;i<name_len;i++){
		delete[] act_adjlist[i].adj;
		progress(25+i*25/name_len);
	}
	
	delete[] act_adjlist;
	
	progress(25);
	
	delete[] mov_namelist;
	
	progress(75);
	
	for(int i=0;i<akas_len;i++){
		delete[] mov_adjlist[i].adj;
		progress(25+i*25/akas_len);
	}
	
	delete[] mov_adjlist;
	
	progress(100);
	
	cout << "Exiting\n";
}
