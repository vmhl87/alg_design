//  I would have tried to do this in Python, but the sheer \
	size of the data involved was prohibitive. Running on  \
	my PC, this program takes over 4 minutes to complete,  \
	not to mention how long it would take on my laptop.

// import necessary libraries
#include <unordered_set>
#include <iostream>
#include <fstream>
#include <string>
#include <map>
using namespace std;

// helper utility to pretty-print progress bars
void draw_percentage(long long p) {
	cout << "\r[";
	for(long long i=0;i<100;i+=2){
		if(i<p) cout << '=';
		else if(i==p) cout << '-';
		else cout << ' ';
	}
	cout << "] (" << p << "%)  ";
	fflush(stdout);
	if(p>=100) cout << '\n';
}

int main(){
	// initialize input/output streams
	cout << "Opening files\n";

	ifstream names("name.basics.tsv");
	ifstream akas("title.akas.tsv");
	ifstream princ("title.principals.tsv");

	ofstream act_apn("actors_apn.list");
	ofstream act_name("actors_name.list");
	ofstream act_adj("actors_adj.list");
	ofstream mov_apn("movies_apn.list");
	ofstream mov_name("movies_name.list");
	ofstream mov_adj("movies_adj.list");
	
	//  create blank string buffer (it isn't used for \
		anything besides removing unnecessary lines   \
		from the top of files
	string nil;

	// lengths of each file (precomputed)
	const long long name_len = 13205098,
	                akas_len = 38592396,
	                prin_len = 60226529;

	//  initialize first set of datastructures - arrays  \
		to store the names of actors, and the alphanum   \
		(apn) identifiers of movies/actors, and hashmaps \
		to quickly obtain integer indexes of given titles.
	cout << "Creating datastructures\n";

	map<string, int> actor_index;
	map<string, int> movie_index;
	//  note that these variables are initialized on the heap \
		due to their extreme size
	string *movies_apn = new string[akas_len];
	string *movies_name = new string[akas_len];
	string *actors_apn = new string[name_len];
	string *actors_name = new string[name_len];

	// read in from names.basics.tsv
	cout << "Reading actors\n";

	//  get rid of first line - specifies field values, which we \
		don't need to parse
	getline(names, nil);

	// prc (percent) used for progress bar
	long long prc=0; draw_percentage(0);
	for(long long i=0;i<name_len;i++){
		// input entire line
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
		// calculate percent value and print if changed
		long long nprc = (i*100+100)/name_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}

	// read from title.akas.tsv (stores name of movie and apn)
	cout << "Reading titles\n";
	
	// trim
	getline(akas, nil);

	prc=0; draw_percentage(0);
	for(long long i=0;i<akas_len;i++){
		string s; getline(akas, s);
		//  similar to how we parsed names.basics.tsv, except \
			there is an extra symbol between name and apn, so \
			we store swaps as an integer count instead of bool
		int sw=0;
		for(char c:s){
			if(c=='	'){
				if(sw==2) break;
				sw++; continue;
			}
			// append character to correct string
			if(sw==0) movies_apn[i] += c;
			if(sw==2) movies_name[i] += c;
		}
		movie_index[movies_apn[i]] = i;
		long long nprc = (i*100+100)/akas_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}

	// write apn orderings to file so we can delete their vars
	cout << "Writing orders to file\n";

	// progress bar
	prc=0; draw_percentage(0);
	long long id=0,sum=name_len*2+akas_len*2;
	
	// write actor alphanumerics to actors_apn.list
	for(long long i=0;i<name_len;i++){
		// write through act_apn (std::ostream)
		act_apn << actors_apn[i] << '\n';
		long long nprc = (id++*100+100)/sum;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	// close file; we are done using it
	act_apn.close();

	// write actor names to actors_name.list
	for(long long i=0;i<name_len;i++){
		act_name << actors_name[i] << '\n';
		long long nprc = (id++*100+100)/sum;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	act_name.close();

	// write movie alphanumerics to movies_apn.list
	for(long long i=0;i<akas_len;i++){
		mov_apn << movies_apn[i] << '\n';
		long long nprc = (id++*100+100)/sum;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	mov_apn.close();
	
	// write movie names to movies_name.list
	for(long long i=0;i<akas_len;i++){
		mov_name << movies_name[i] << '\n';
		long long nprc = (id++*100+100)/sum;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	mov_name.close();

	// clean up unnecessary arrays
	cout << "Deleting arrays\n";
	
	draw_percentage(0);

	//  note that we are using c++ and must explicitly delete \
		variables that are allocated on the heap
	delete[] actors_apn;

	draw_percentage(25);

	delete[] actors_name;

	draw_percentage(50);

	delete[] movies_apn;
	
	draw_percentage(75);

	delete[] movies_name;

	draw_percentage(100);
	
	// build adjacency lists for movies and actors
	cout << "Building adjacencies\n";

	//  we will store these adjacency lists as arrays of sets;  \
		actor_adj stores a set for each actor, consisting of    \
		the movies adjacent to it, and movie_adj stores a set   \
		for each movie, consisting of its adjacent actors. note \
		that these are again heap allocated arrays
	unordered_set<int> *actor_adj = new unordered_set<int>[name_len];
	unordered_set<int> *movie_adj = new unordered_set<int>[akas_len];

	//  now we need to read from titles.principals.tsv, which     \
		tells us which actors serve what position in what movies. \
		We don't care about their characters' names or positions, \
		only alphanumeric identifiers.
	cout << "Linking\n";
	
	// again we cannot parse the top line
	getline(princ, nil);

	prc=0; draw_percentage(0);
	for(long long i=0;i<prin_len;i++){
		string s; getline(princ, s);
		// declare variables for movie apn and actor name
		string apn, name;
		// similar to how we parsed movie titles
		int sw = 0;
		// not all entries in principals are actors
		bool actor = 0;
		for(char c:s){
			if(c=='	'){
				sw++; continue;
			}
			if(sw==0) apn += c;
			if(sw==2) name += c;
			if(sw==3){
				//  if three swaps have happened, we are at the   \
					entry storing the position of the actor - and \
					if it starts with 'a' they are an actor/actress
				if(c=='a') actor=1;
				break;
			}
		}
		// if the character was an actor, insert into adjacency sets
		if(actor){
			//  here we use the indexing hashmaps to convert from apn \
				to integer index efficiently
			actor_adj[actor_index[name]]
			    .insert(movie_index[apn]);
			movie_adj[movie_index[apn]]
			    .insert(actor_index[name]);
		}
		// progress bar
		long long nprc = (i*100+100)/prin_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	
	// write adjacency sets to file
	cout << "Writing to files\n";
	
	//  write actor adjacency lists to actor_adj.list through \
		act_adj (std::ostream)
	prc=0; draw_percentage(0);
	for(long long i=0;i<name_len;i++){
		//  print out number of adjacent actors
		act_adj << actor_adj[i].size();
		// loop through std::unordered_set<T> with an iterator, and print
		for(auto x=actor_adj[i].begin();x!=actor_adj[i].end();x++){
			act_adj << ' ' << *x;
		}
		// print newline
		act_adj << '\n';
		// progress
		long long nprc = (i*100+100)/name_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	// close file
	act_adj.close();
	
	// same thing, but for movie adj sets
	prc=0; draw_percentage(0);
	for(long long i=0;i<akas_len;i++){
		mov_adj << movie_adj[i].size();
		for(auto x=movie_adj[i].begin();x!=movie_adj[i].end();x++){
			mov_adj << ' ' << *x;
		}
		mov_adj << '\n';
		long long nprc = (i*100+100)/akas_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	mov_adj.close();

	//  cleanup adjacency lists - note that our hashmaps are allocated \
		on the stack and do not need to be explicitly deallocated
	cout << "Cleaning\n";
	
	draw_percentage(0);
	
	delete[] actor_adj;
	
	draw_percentage(50);
	
	delete[] movie_adj;

	draw_percentage(100);

	// hopefully the program got here without issues!
	cout << "Exiting\n";
}
