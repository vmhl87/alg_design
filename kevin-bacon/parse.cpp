#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
using namespace std;

int main(){
	cout << "Opening files\n";

	ifstream names("names.basics.tsv");
	ifstream akas("titles.akas.tsv");
	ifstream princ("titles.principals.tsv");

	ofstream mov("movies.list");
	ofstream act_apn("actors_apn.list");
	ofstream act_name("actors_name.list");

	const int name_len = 13205099,
	          akas_len = 38592397,
	          prin_len = 60226530;

	cout << "Creating datastructures\n";

	map<string, int> actor_index;
	map<string, int> movie_index;
	string *movies = new string[akas_len];
	string *actors_apn = new string[name_len];
	string *actors_name = new string[name_len];

	cout << "Reading actors\n";

	int prc=0;
	for(int i=0;i<name_len;i++){
		string s; names >> s;
		bool sw=0;
		for(char c:s){
			if(c==' '){
				if(sw) break;
				sw = 1;
			}
			if(sw) actors_name[i] += c;
			else actors_apn[i] += c;
		}
		actor_index[actors_apn[i]] = i;
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
		for(char c:s){
			if(c==' ') break;
			movies[i] += c;
		}
		movie_index[movies[i]] = i;
		int nprc = (i*10+10)/akas_len;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Writing orders to file\n";

	prc=0;
	int id=0,sum=name_len*2+akas_len;
	for(int i=0;i<name_len;i++){
		act_apn << actors_apn[i] << '\n';
		int nprc = (id++*10+10)/sum;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	for(int i=0;i<name_len;i++){
		act_name << actors_name[i] << '\n';
		int nprc = (id++*10+10)/sum;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	for(int i=0;i<akas_len;i++){
		mov << movies[i] << '\n';
		int nprc = (id++*10+10)/sum;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Deleting arrays\n";

	delete[] actors_apn;

	cout << "25%\n";

	delete[] actors_name;

	cout << "50%\n";

	delete[] movies;

	cout << "100%\n";

	vector<int> *has = new vector<int>[name_len];

	cout << "Linking\n";

	prc=0;
	for(int i=0;i<prin_len;i++){
		string s; princ >> s;
		string apn, name;
		int sw = 0;
		bool actor = 0;
		for(char c:s){
			if(c==' '){
				sw++; continue;
			}
			if(sw==0) apn += c;
			if(sw==2) name += c;
			if(sw==3){
				if(c=='a') actor=1;
				break;
			}
		}
		if(actor){
			has[actor_index[name]]
			    .push_back(movie_index[name]);
		}
		int nprc = (i*10+10)/prin_len;
		if(nprc>prc){
			cout << nprc*10 << "%\n";
			prc = nprc;
		}
	}

	cout << "Formatting\n";

	vector<bool> *adj = new vector<bool>(akas_len)[akas_len];

	cout << "Grouping\n";

	prc=0;
	for(int i=0;i<name_len;i++){
		int group_size = has[i].size();
		for(int a:has[i]){
			for(int b:has[i]){
				adj[a][b] = 1;
			}
		}
		int nprc=(i*20+20)/name_len;
		if(nprc>prc){
			cout << nprc*5 << "%\n";
			prc = nprc;
		}
	}

	cout << "Cleaning arrays\n";

	delete[] has;

	cout << "50%";

	delete[] adj;

	cout << "100%\n";

	cout << "Exiting\n";
}
