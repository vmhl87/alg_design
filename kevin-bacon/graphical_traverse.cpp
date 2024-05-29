// libraries
#include <unordered_set>
#include <signal.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stack>
#include <queue>
#include <cmath>

// framebuffer GUI libraries  -  https://github.com/vmhl87/fbgui
#include "tgui.c"
#include "tgin.c"

// transitional datastructures - static node & traverse node
typedef struct{
	int id;
	int n_adj;
	int *adj;
	bool init = 0;
} node;

typedef struct{
	int id;
	int depth;
	int from;
	bool is_act = 1;
} traverse_node;

// fancy progress bars
long long prc=100;
void progress(long long p) {
	if(p==100||p>prc||(p==0&&prc>0)){}else return;
	if(p==0)rect(width/2 - 150, height/2 + 24, 300, 10, 190, 190, 190);
	rect(width/2 - 150+prc*3, height/2 + 24, 3*(p-prc), 10, 0, 0, 0);
	prc=p;
}

// kb interrupts
volatile sig_atomic_t signal_status = 0;

void sighandler(int s) {signal_status = s;}

// actor, apn counts
const long long name_len = 13205098,
	            akas_len = 38592396;

// global pointers to heap arrays
node *al, *vl;

// because of memory constraints, we don't store the names of each individual
// movie and actor. We instead dynamically locate on the fly given integer ID.

// find integer ID from actor name
int get_actor(std::string name){
	std::ifstream act_name("actors_name.list");
	for(int i=0; i<name_len; ++i){
		if(signal_status == SIGINT){
			act_name.close();
			return -2;
		}
		std::string s; getline(act_name, s);
		if(s == name){
			act_name.close();
			return i;
		}
		progress(std::min(((std::__lg(i)-6)*100/(std::__lg((int)name_len)-6)),
			100));
	}
	act_name.close();
	return -1;
}

std::string ist(int i){
	std::string ret;
	while(i){
		ret = (char)('0' + i%10) + ret;
		i /= 10;
	}
	return ret;
}

// find actor name from integer ID
std::string actor_name(int id, int r, int p){
	std::string fname = "actors_name.list";
	std::ifstream act_name(fname);
	std::string name;
	for(int i=0; i<=id; ++i){
		getline(act_name, name);
		progress(r + i*p/id);
	}
	act_name.close();
	return name;
}

// find movie name from ID: we splitbuffer this because some titles
// seem to have UTF8 which drastically slows down the parse speed
std::string movie_name(int id, int r, int p){
	std::string fname = "movie_names/" + ist(id/100000) + ".list";
	std::ifstream mov_name(fname);
	id %= 100000;
	std::string name;
	for(int i=0; i<=id; ++i){
		getline(mov_name, name);
		progress(r + i*p/id);
	}
	mov_name.close();
	return name;
}

// various allocators (helper functions)
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

traverse_node actor_node_at(int id) {
	return actor_node_at(id, 0, -1);
}

traverse_node movie_node_at(int id) {
	return movie_node_at(id, 0, -1);
}

// drawing utilities - redraw various segments of the UI when updated
void drec(){
	rect(width/2 - 160, height/2 - 40, 320, 80, 170, 170, 170);
}

void drech(){
	rect(width/2 - 160, height/2 - 40, 320, 44, 170, 170, 170);
}

int notdre(int x, int y){
	if(x >= width/2 - 160 && y >= height/2 - 40 &&
		x <= width/2 + 160 && y <= height/2 + 40)
		return to_color(170, 170, 170);
	if(x >= width/2 - 158 && y >= height/2 - 38 &&
		x <= width/2 + 162 && y <= height/2 + 42)
		return to_color(50, 50, 50);
	return to_color(150, 150, 100);
}

void sstrx(const char *s, int x, int y, int c, int r, int g, int b){
	sstr(s, x+(strlen(s)<<2), y, c, r, g, b);
}

void sstr(std::string s, int x, int y, int c, int r, int g, int b){
	sstr(s.c_str(), x, y, c, r, g, b);
}

void sstrx(std::string s, int x, int y, int c, int r, int g, int b){
	sstrx(s.c_str(), x, y, c, r, g, b);
}

// leaderboard!
std::pair<int, std::string> leaderboard[3];

void drect(){
	shade(8, 8, width-16, height-16, notdre);
	sstr("The Bacon Number", width/2+2, 52, 6, 0, 0, 0);
	sstr("The Bacon Number", width/2, 50, 6, 78, 42, 132);
	int mwi = 20;
	mwi = std::max(mwi, 3+(int)leaderboard[0].second.length()+12);
	mwi = std::max(mwi, 3+(int)leaderboard[1].second.length()+12);
	mwi = std::max(mwi, 3+(int)leaderboard[2].second.length()+12);
	rect(width/2 - mwi*4-6, height-110, (mwi<<3)+16, 88, 50, 50, 50);
	rect(width/2 - mwi*4-8, height-112, (mwi<<3)+16, 88, 170, 170, 170);
	sstr("Longest paths found:", width/2, height-104, 1, 0, 0, 0);
	sstrx("1.", width/2-4*mwi, height-80, 1, 0, 0, 0);
	sstrx(leaderboard[0].second, width/2-4*mwi+24, height-80, 1, 0, 0, 0);
	sstrx(", distance ", width/2-4*mwi+24+8*leaderboard[0].second.length(), height-80, 1, 0, 0, 0);
	char v[4]; sprintf(v, "%d", leaderboard[0].first);
	sstrx(v, width/2-4*mwi+24+8*leaderboard[0].second.length()+88, height-80, 1, 0, 0, 0);
	sstrx("2.", width/2-4*mwi, height-64, 1, 0, 0, 0);
	sstrx(leaderboard[1].second, width/2-4*mwi+24, height-64, 1, 0, 0, 0);
	sstrx(", distance ", width/2-4*mwi+24+8*leaderboard[1].second.length(), height-64, 1, 0, 0, 0);
	sprintf(v, "%d", leaderboard[1].first);
	sstrx(v, width/2-4*mwi+24+8*leaderboard[1].second.length()+88, height-64, 1, 0, 0, 0);
	sstrx("3.", width/2-4*mwi, height-48, 1, 0, 0, 0);
	sstrx(leaderboard[2].second, width/2-4*mwi+24, height-48, 1, 0, 0, 0);
	sstrx(", distance ", width/2-4*mwi+24+8*leaderboard[2].second.length(), height-48, 1, 0, 0, 0);
	sprintf(v, "%d", leaderboard[2].first);
	sstrx(v, width/2-4*mwi+24+8*leaderboard[2].second.length()+88, height-48, 1, 0, 0, 0);
	attr(BG(WHITE)); attr(BLACK);
}

// helper function for length of integer as a std::string literal
int lin(int i){
	int x=0;
	while(i > 0) ++x, i /= 10;
	return x;
}

// overloads for input that can't be done in pure c
void center(const char *s){
	center(s, W_CHARS/2, H_CHARS/2);
}

void center(std::string s){
	center(s.c_str());
}

std::string text_box(int x, int y, int w){
	char *str;
	text_box(&str, x, y, w);
	std::string ret;
	ret.assign(str);
	return ret;
}

int target_id = 101;
std::string target_name = "Kevin Bacon";

// wrapper for entire search routine
void search(){
	// textbox input and UI to read in actor
	drect();
	center("Enter the name of an actor:");
	attr(NONE);
	rect((W_CHARS/2-18)*W_CHAR-4, (1+H_CHARS/2)*H_CHAR-4,
		(width/2-(W_CHARS/2-18)*W_CHAR+4)*2, H_CHAR + 8, 0, 0, 0);
	std::string actor = text_box(W_CHARS/2 - 17, H_CHARS/2 + 2, 36);
	attr(BG(WHITE)); attr(BLACK);

	// exit command with hardcoded visual sequence
	if(actor == "exit"){
		drec();
		center("Synchronizing shutdown sequence...");
		progress(100);
		progress(0), sleepms(200);
		progress(10), sleepms(100);
		progress(40), sleepms(300);
		progress(45), sleepms(600);
		progress(70), sleepms(200);
		progress(75), sleepms(100);
		progress(80), sleepms(500);
		progress(100);
		return;
	}
	
	// escape cmds
	if(actor.size() && actor[0] == '%'){
		if(actor.size() > 1){
			if(actor[1] == 'r'){
				attr(NONE);
				system("clear");
				attr(BG(WHITE));
				drect();
				search();
				return;
			}
			if(actor[1] == 'w'){
				std::ofstream lbstream("leaderboard.txt");
				for(int i=0; i<3; ++i){
					lbstream << leaderboard[i].first << ' ' <<
						leaderboard[i].second << '\n';
				}
				lbstream.close();
				drect();
				search();
				return;
			}
			if(actor[1] == 's' && actor.size() > 2 && actor[2] == ' '){
				std::string nt = "";
				for(int i=3; i<actor.size(); ++i){
					nt += actor[i];
				}
				drec();
				center("Updating target...");
				progress(0);
				int ntid = get_actor(nt);
				if(ntid == -1){
					drec();
					center("Not found");
					sleepms(1000);
					search();
					return;
				}else{
					target_id = ntid;
					target_name = nt;
					drech();
					center("Target updated");
					sleepms(1000);
					progress(100);
					search();
					return;
				}
			}
			search();
			return;
		}
	}

	// search for actor ID from actor name
	drec();
	move(W_CHARS/2 - (22 + actor.length())/2 + 1, H_CHARS/2);
	printf("Searching for ");
	attr(BLUE);
	printf(actor.c_str());
	attr(BLACK);
	printf(" in list");
	fflush(stdout);
	
	progress(0);

	signal(SIGINT, sighandler); signal_status = 0;
	int actor_id = get_actor(actor);
	signal(SIGINT, SIG_DFL);

	sleepms(100);

	// process if found
	if(actor_id >= 0){
		drech();
		move(W_CHARS/2 - (16 + actor.length() + lin(actor_id))/2 + 1, H_CHARS/2);
		printf("Found ");
		attr(BLUE);
		printf(actor.c_str());
		attr(BLACK);
		printf(" at index ");
		attr(BLUE);
		printf("%d", actor_id);
		attr(BLACK);
		fflush(stdout);
		
		sleepms(1000);
		progress(100);
	}else if(actor_id == -2){
		drec();
		center("Aborted");
		center("Press enter to run again", W_CHARS/2, H_CHARS/2 + 1);

		std::string s; getline(std::cin, s);

		progress(100);
		search();
		return;
	}else{
		drec();
		move(W_CHARS/2 - (22 + actor.length())/2 + 1, H_CHARS/2);
		printf("Couldn't find ");
		attr(BLUE);
		printf(actor.c_str());
		attr(BLACK);
		printf(" in list");
		center("Press enter to run again", W_CHARS/2, H_CHARS/2 + 1);

		std::string s; getline(std::cin, s);

		// rerun
		progress(100);
		search();
		return;
	}

	// setup datastructures for traversal
	drec();

	std::vector<traverse_node> search_queue;
	int front_index = 0;
	
	std::unordered_set<int> actors_visited;
	std::unordered_set<int> movies_visited;
	
	search_queue.push_back(actor_node_at(actor_id));
	actors_visited.insert(actor_id);

	// begin traversal
	drec();
	center("Traversing graph");

	progress(0);

	sleepms(800);

	progress(7);
	
	int iter = 0, depth = 0;
	traverse_node front = search_queue[0];
	
	int found_target = 0;
	if(actor == target_name) found_target = 1;
	
	// DFS loop
	signal(SIGINT, sighandler); signal_status = 0;
	while(found_target == 0 && front_index < search_queue.size()){
		if(signal_status == SIGINT){
			found_target = 2;
			break;
		}

		front = search_queue[front_index];
		++front_index;
			
		bool finished = 0;
		
		if(front.is_act){
			if(al[front.id].init) for(int i=0;i<al[front.id].n_adj;i++){
				if(movies_visited.find(al[front.id].adj[i])
					!=movies_visited.end()) continue;
				movies_visited.insert(al[front.id].adj[i]);
				search_queue.push_back(
					movie_node_at(al[front.id].adj[i], front.depth+1, iter)
				);
			}
		}else{
			if(vl[front.id].init) for(int i=0;i<vl[front.id].n_adj;i++){
				if(actors_visited.find(vl[front.id].adj[i])
					!=actors_visited.end()) continue;
				actors_visited.insert(vl[front.id].adj[i]);
				search_queue.push_back(
					actor_node_at(vl[front.id].adj[i], front.depth+1, iter)
				);
				if(vl[front.id].adj[i] == target_id){
					front = search_queue[search_queue.size()-1];
					found_target = 1;
					break;
				}
			}
		}

		if(found_target) break;

		depth = front.depth;
		
		if(iter%576==0) progress(std::min(7 + (std::__lg(iter)-8) * 7, 100));
		
		++iter;
	}
	signal(SIGINT, SIG_DFL);
	
	// process no path found
	if(found_target != 1){
		drec();
		if(found_target == 0) center("Couldn't find a path!");
		else center("Traversal aborted");
		center("Press enter to run again", W_CHARS/2, H_CHARS/2 + 1);

		std::string s; getline(std::cin, s);

		// rerun
		progress(100);
		search();
		return;
	}
	
	drech();
	std::string re = "Found " + target_name;
	center(re);

	sleepms(800);

	// backtrace to find exact actors/movies touched
	progress(100);
	drec();
	center("Retrieving path...");

	progress(0);
	
	std::stack<traverse_node> path;
	
	while(front.from+1 && depth--> -3){
		path.push(front);
		front = search_queue[front.from];
	}
	
	std::queue<std::string> vls;
	
	vls.push(actor);

	int sw = 24, ln = path.size(), x = 0;
	
	while(!path.empty()){
		traverse_node node = path.top();
		path.pop();
		
		if(node.is_act){
			std::string name = actor_name(node.id, x*100/ln, 100/ln);
			sw = (name.length() > sw ? name.length() : sw);
			vls.push(name);
			if(node.id == target_id) break;
		}else{
			std::string name = "(" + movie_name(node.id, x*100/ln, 100/ln) + ")";
			sw = (name.length() > sw ? name.length() : sw);
			vls.push(name);
		}
		
		progress((++x)*100/ln);
	}

	progress(100);
	
	sleepms(800);
	
	rect(8, 8, width-16, height-16, 150, 150, 100);

	int lines = vls.size()*3 + 5;

	rect(width/2 - sw*W_CHAR/2 - 21, height/2 - lines*H_CHAR/2 - 13,
		sw*W_CHAR + 48, lines*H_CHAR + 32, 60, 60, 60);
	rect(width/2 - sw*W_CHAR/2 - 24, height/2 - lines*H_CHAR/2 - 16,
		sw*W_CHAR + 48, lines*H_CHAR + 32, 170, 170, 170);

	// pretty print result
	move(W_CHARS/2 - 11, (height/2 - 16)/H_CHAR + lines/2 + 1);
	printf("Press enter to run again\n");

	int yval = (height/2 - 16)/H_CHAR - lines/2 + 2,
		par = 0;

	bool record = 0;
	if(target_id == 101){
		int len = vls.size()>>1, slen = len;

		for(int i=0; i<3; ++i){
			if(leaderboard[i].second == actor) break;
			if(leaderboard[i].first < slen){
				std::string tmp = leaderboard[i].second + "";
				leaderboard[i].second =  actor + "";
				actor = tmp + "";
				slen = leaderboard[i].first + 1;
				leaderboard[i].first = len;
				len = slen - 1;
				record = 1;
			}
		}
	}

	while(!vls.empty()){
		int xv = width/2 - vls.front().size()*4 + 8;
		if(par){
			_vline(width/2, (yval-3)*H_CHAR + 12, (yval+1)*H_CHAR + 4,
				100, 100, 100);
			_hline(width/2-2, width/2+2, (yval+1)*H_CHAR + 2, 100, 100, 100);
			_vline(width/2, yval*H_CHAR-20, yval*H_CHAR+4, 150, 150, 150);
			sstr(vls.front(), width/2, yval*H_CHAR-16, 1, 50, 50, 50);
		}else{
			rectl(xv-8 - 4, (yval-1)*H_CHAR - 4,
				vls.front().size()*W_CHAR + 8, H_CHAR + 8, 50, 50, 50);
			if(vls.front() == target_name) rectl(xv-8 - 4,
				(yval-1)*H_CHAR - 4, vls.front().size()*W_CHAR + 8, H_CHAR + 8,
				0, 0, 170);
			sstr(vls.front(), width/2, yval*H_CHAR-16, 1, 0, 0, 0);
		}
		par ^= 1;
		yval += 3;
		vls.pop();
	}

	if(record){
		if(0){
			std::ofstream lbstream("leaderboard.txt");
			for(int i=0; i<3; ++i){
				lbstream << leaderboard[i].first << ' ' <<
					leaderboard[i].second << '\n';
			}
			lbstream.close();
		}
		rectl(16, height-46+28-6, 16*9-3, 6, 0, 100, 0);
		_hline(19, 154, height-46+28-6, 150, 150, 100);
		sstrx("Wow, new record!", 24, height-38, 1, 0, 0, 0);
	}

	// rerun
	move(0, 0);
	std::string r; getline(std::cin, r);
	search();
}

int fromst(char *s){
	int ret = 0;
	for(int i=0; i<strlen(s); ++i){
		ret = ret*10 + (s[i] - '0');
	}
	return ret;
}

// setup/cleanup global arrays & datasets
int main(int argc, char *argv[]) {
	// read leaderboard
	std::ifstream lbstream("leaderboard.txt");
	for(int i=0; i<3; ++i)
		lbstream >> leaderboard[i].first, lbstream.ignore(1),
			getline(lbstream, leaderboard[i].second);
	lbstream.close();
	
	// setup FBGUI
	curs_set(0);
	system("clear");
	openfb();

	if(argc>2){
		int _LW = fromst(argv[1]),
			_LH = fromst(argv[2]);
		width -= W_CHAR * (_LW*2 + 1) / 2, height -= H_CHAR * (_LH*2 + 1) / 2;
		W_CHARS -= _LW, H_CHARS -= _LH;
	}

	// initial background
	drect();

	// pretty-print startup sequence
	attr(BG(WHITE)); attr(BLACK);
	center("Booting...");

	progress(0), sleepms(200);
	progress(10), sleepms(100);
	progress(40), sleepms(300);
	progress(45), sleepms(600);
	progress(70), sleepms(200);
	progress(75), sleepms(100);
	progress(80), sleepms(500);
	progress(100);

	sleepms(800);

	// begin reading from adj lists
	drec();
	center("Opening file streams");

	progress(0);
	
	sleepms(200);

	std::ifstream act_adj("actors_adj.list");
	std::ifstream mov_adj("movies_adj.list");
	
	progress(100);

	sleepms(800);

	// prepare datastructures with correct length & ids
	drec();
	center("Creating datastructures");
	
	progress(0);
	
	node *act_adjlist = new node[name_len];
	
	for(int i=0;i<name_len;i++){
		act_adjlist[i].id = i;
		progress(i*100/(name_len+akas_len));
	}
	
	al = act_adjlist;
	
	node *mov_adjlist = new node[akas_len];
	
	for(int i=0;i<akas_len;i++){
		mov_adjlist[i].id = i;
		progress((name_len+i+1)*100/(name_len+akas_len));
	}
	
	vl = mov_adjlist;

	// read from file streams and compose into adjacency lists
	// Note: These arrays are represented with perhaps the std::minimum amount
	// of memory necessary, but are absolutely massive. At 3.2gb they just
	// about use all of the RAM on this system, with no other GUI running.
	drec();
	center("Building adjacency lists");
	
	for(int i=0;i<name_len;i++){
		int n_adjacent; act_adj >> n_adjacent;
		act_adjlist[i].n_adj = n_adjacent;
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

	sleepms(500);

	// cleanup hanging file streams
	drec();
	center("Closing file streams");

	progress(0);

	sleepms(500);
	
	act_adj.close();
	mov_adj.close();
	
	progress(100);

	sleepms(1000);
	
	// start the search loop
	search();

	// when done searching, start cleanup
	drec();
	center("Deleting datastructures");
	
	progress(0);
	
	// each heap array is itself a heap array so we need to delete every one
	for(int i=0;i<name_len;i++){
		delete[] act_adjlist[i].adj;
		progress(i*25/name_len);
	}
	
	delete[] act_adjlist;
	
	progress(30);
	
	for(int i=0;i<akas_len;i++){
		delete[] mov_adjlist[i].adj;
		progress(30+i*55/akas_len);
	}
	
	delete[] mov_adjlist;
	
	progress(100);

	sleepms(800);

	blank();
	
	// cleanup FBGUI and return console to normal state
	closefb();
	attr(NONE);
	system("clear");
	curs_set(1);
}
