#include <iostream>
#include <vector>
using namespace std;

struct atom_node{
	char sym[2];
	struct atom* next[4];
	int n_next=0;
	int bond_types[4];
};

struct atom{
	char sym[2];
	int n_bonds;
};

struct formula{
	vector<struct atom> types;
	vector<int> count;
};

void append_atom(struct formula in,char sym[],int n_bonds,int count){
	struct atom tmp;tmp.sym[0]=sym[0];tmp.sym[1]=sym[1];tmp.n_bonds=n_bonds;
	in.types.push_back(tmp);in.count.push_back(count);
}

struct argv{
        int* counts;
        int n_types;
        int* bond_mult;
        int* bond_from;
        struct atom_node* pushed;
        int len;
        int look=0;
        int alloc=0;
};

void find_molecules(struct formula in,vector<struct atom_node[]> out){
	int n_types=in.count.size(),len=0;
	int counts[n_types];for(int i=0;i<n_types;i++){len+=in.count[i];counts[i]=in.count[i];}
	// init inital array and begin recurse
	struct argv args;args.counts=&counts;args.n_types=n_types;args.len=len;
	int bond_mult[len],bond_from[len];struct atom_node pushed[len];args.bond_mult=&bond_mult;args.bond_from=&bond_from;args.pushed=&pushed;
	for(int i=0;i<len;i++)bond_from[i]=-1;
	recursively_step(in,out,args);
}

void recursively_step(struct formula in,vector<struct atom_node[]> out,struct argv args){
	
}

int main(){
	// input conditions: C2 H4 O2
	struct formula in;char a[3][2]={{'C','.'},{'H','.'},{'O','.'}};append_atom(in,a[0],4,2);append_atom(in,a[1],1,4);append_atom(in,a[2],2,2);
	vector<struct atom_node[]> out;
	find_molecules(in,out);
	// do something with out
	return 0;
}
