#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

typedef struct{
	int id;
	vector<int> adj;
} node;

long long prc=100;
void progress(long long p) {
	if(p==100||p>prc||(p==0&&prc>0)) prc = p;
	else return;
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
	cout << "Opening files\n";

	ifstream act_apn("actors_apn.list");
	ifstream act_name("actors_name.list");
	ifstream act_adj("actors_adj.list");
	ifstream mov_apn("movies_apn.list");
	ifstream mov_name("movies_name.list");
	ifstream mov_adj("movies_adj.list");
	
	const long long name_len = 13205098,
	                akas_len = 38592396,
	                prin_len = 60226529;
	
	progress(100);
	
	cout << "Creating datastructures\n";
	
	node *act_adjlist = new node[name_len];
	
	for(int i=0;i<name_len;i++){
		act_adjlist[i].id = i;
		progress(i*100/(name_len+akas_len));
	}
	
	node *mov_adjlist = new node[akas_len];
	
	for(int i=0;i<akas_len;i++){
		mov_adjlist[i].id = i;
		progress((name_len+i+1)*100/(name_len+akas_len));
	}
	
	cout << "Building adjacency lists\n";
	
	progress(100);
	
	cout << "Deleting datastrucutres\n";
	
	progress(0);
	
	delete[] act_adjlist;
	
	progress(50);
	
	delete[] mov_adjlist;
	
	progress(100);
	
	cout << "Exiting\n";
}
