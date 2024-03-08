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
		if(i<p-1) cout << '=';
		else if(i==p-1) cout << '-';
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

	ofstream names_thin("name_thinned.basics.tsv");
	ofstream akas_thin("title_thinned.akas.tsv");
	ofstream princ_thin("title_thinned.principals.tsv");
	
	//  create blank string buffer (it isn't used for \
		anything besides removing unnecessary lines   \
		from the top of files
	string nil;

	// lengths of each file (precomputed)
	const long long name_len = 13205098,
	                akas_len = 38592396,
	                prin_len = 60226529;

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
				sw = 1;
			}
			names_thin << c;
		}
		names_thin << '\n';
		// calculate percent value and print if changed
		long long nprc = (i*100+100)/name_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	names_thin.close();

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
		int sw=0, priority=0;
		string lang;
		for(char c:s){
			if(c=='	'){
				if(sw==3) break;
				sw++;
			}
			akas_thin << c;
		}
		akas_thin << '\n';
		long long nprc = (i*100+100)/akas_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	akas_thin.close();
	
	cout << "Linking\n";
	
	// again we cannot parse the top line
	getline(princ, nil);

	prc=0; draw_percentage(0);
	for(long long i=0;i<prin_len;i++){
		string s; getline(princ, s);
		// declare variables for movie apn and actor name
		string apn, name, actor;
		// similar to how we parsed movie titles
		int sw = 0;
		for(char c:s){
			if(c=='	'){
				if(sw==3) break;
				sw++;
			}
			princ_thin << c;
		}
		princ_thin << '\n';
		// progress bar
		long long nprc = (i*100+100)/prin_len;
		if(nprc>prc){
			draw_percentage(nprc); prc = nprc;
		}
	}
	princ_thin.close();

	// hopefully the program got here without issues!
	cout << "Exiting\n";
}
