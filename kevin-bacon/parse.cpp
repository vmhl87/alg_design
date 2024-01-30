#include <iostream>
#include <fstream>
#include <string>
#include <unordered_set>
#include <map>
using namespace std;

typedef struct{
	string name;
	string apn;	
}actor;

typedef struct{
	string name;
	string apn;
	unordered_set<string> actors;
}movie;

int main(){
	cout << "Opening files\n";

	ifstream names("names.basics.tsv");
	ifstream akas("titles.akas.tsv");
	ifstream princ("titles.principals.tsv");

	int name_len = 13205099,
	    akas_len = 38592397,
	    prin_len = 60226530;

	cout << "Creating arrays\n";

	actor *actors = new actor[name_len];
	movie *movies = new movie[akas_len];
	map<string, int> actor_index;
	map<string, int> movie_index;

	cout << "Reading actors\n";

	int prc=0;
	for(int i=0;i<name_len;i++){
		string s; names >> s;
		bool sw = 1;
		for(char c:s){
			if(c==' '){
				if(sw) break;
				sw = 1; continue;
			}
			if(sw) actors[i].name += c;
			else actors[i].apn += c;
		}
		actor_index[actors[i].apn] = i;
		int nprc = (i*10+10)/name_len;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Reading titles\n";

	prc=0;
	for(int i=0;i<akas_len;i++){
		string s; akas >> s;
		string apn, name;
		int sw = 0;
		for(char c:s){
			if(c==' '){
				if(sw==2) break;
				sw++; continue;
			}
			if(sw==0) movies[i].apn += c;
			if(sw==2) movies[i].name += c;
		}
		movie_index[movies[i].apn] = i;
		int nprc = (i*10+10)/akas_len;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Linking\n";

	prc=0;
	for(int i=0;i<prin_len;i++){
		string s; princ >> s;
		string apn, name;
		int sw = 0;
		for(char c:s){
			if(c==' '){
				if(sw==2) break;
				sw++; continue;
			}
			if(sw==0) apn += c;
			if(sw==2) name += c;
		}
		movies[movie_index[name]].actors.insert(apn);
		int nprc = (i*10+10)/prin_len;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Finished!\n";

	cout << "Deleting arrays\n";

	delete[] actors;

	cout << "50%\n";

	delete[] movies;

	cout << "Exiting\n";
}
