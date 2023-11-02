#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

#define lines 2169

struct e{
	float r;
	float g;
	float b;
	int id;
};

struct e emojis[lines];

struct node{
	float r;
	float g;
	float b;
	float bounds[3][2];
	bool end=false;
	bool finalized=false;
	int next[2][2][2];
};

vector<struct node> tree;

float avg_range(float bounds[3][2],int i){
	float r=0.,g=0.,b=0.;
	for(struct e h:emojis){
		r+=h.r;
		g+=h.g;
		b+=h.b;
	}
	r/=(float)lines;
	g/=(float)lines;
	b/=(float)lines;
	if(i==0)return r;
	if(i==1)return g;
	return g;
}

bool in_bounds(struct e h,float bounds[3][2]){
	if(h.r<bounds[0][0]||h.r>bounds[0][1])return false;
	if(h.g<bounds[1][0]||h.g>bounds[1][1])return false;
	if(h.b<bounds[2][0]||h.b>bounds[2][1])return false;
	return true;
}

void propagate(float r,float g,float l,int i){
	int counts[2][2][2];
	for(struct e h:emojis){
		if(in_bounds(h,tree[i].bounds)){
			int id[3]={h.r>r?1:0,h.g>g?1:0,h.b>l?1:0};
			counts[id[0]][id[1]][id[2]]++;
		}
	}
	for(int a=0;a<2;a++)
		for(int b=0;b<2;b++)
			for(int c=0;c<2;c++)
				if(counts[a][b][c]<2){
					int h=tree.size();
					struct node tmp;
					tmp.end=true;
					tmp.finalized=true;
					// write id of emoji to tmp.next[0][0][0]
					if(counts[a][b][c]==0){
						for(int j=0;j<lines;j++)if(in_bounds(emojis[j],tree[i].bounds)){
							tmp.next[0][0][0]=j;
							break;
						}
					}else{
						float bnd[3][2]={
							{tree[i].bounds[0][0],tree[i].bounds[0][1]},
							{tree[i].bounds[1][0],tree[i].bounds[1][1]},
							{tree[i].bounds[2][0],tree[i].bounds[2][1]}};
						bnd[0][a]=r;bnd[1][b]=g;bnd[2][c]=b;
						for(int j=0;j<lines;j++)if(in_bounds(emojis[j],bnd)){
							tmp.next[0][0][0]=j;
							break;
						}
					}
					tree[i].next[a][b][c]=h;
					tree.push_back(tmp);
				}else{
					int h=tree.size();
					struct node tmp;
					// set bounds
					for(int x=0;x<3;x++)for(int y=0;y<2;y++)tmp.bounds[x][y]=tree[i].bounds[x][y];
					tmp.bounds[0][a]=r;
					tmp.bounds[1][b]=g;
					tmp.bounds[2][c]=l;
					tree[i].next[a][b][c]=h;
					tree.push_back(tmp);
				}
	tree[i].r=r;tree[i].g=g;tree[i].b=l;
	tree[i].finalized=true;
}

void iterate_print(){
	int t=0;
	for(struct node h:tree){
		if(h.end){
			int i=h.next[0][0][0];
			cout<<t<<": ending node "<<i<<" with color "<<emojis[i].r<<' '<<emojis[i].g<<' '<<emojis[i].b<<'\n';
		}else{
			if(h.finalized){
				cout<<t<<": split on "<<h.r<<' '<<h.g<<' '<<h.b<<": goto ";
				for(int a=0;a<2;a++)for(int b=0;b<2;b++)for(int c=0;c<2;c++)cout<<h.next[a][b][c]<<' ';
				cout<<'\n';
			}else{
				cout<<t<<": unfinalized bounds r["<<h.bounds[0][0]<<' '<<h.bounds[0][1]<<"] g[";
				cout<<h.bounds[1][0]<<' '<<h.bounds[1][1]<<"] b["<<h.bounds[2][0]<<h.bounds[2][1]<<"]\n";
			}
		}
		t++;
	}
}

int main(){
	fstream cin("parsed.txt");
	for(int i=0;i<lines;i++){
		char c;cin>>c;
		float f;cin>>f;
		emojis[i].r=f;cin>>c;
		cin>>f;emojis[i].g=f;cin>>c;
		cin>>f;emojis[i].b=f;
		cin>>c;
	}
	for(int i=0;i<lines;i++){
		cout<<emojis[i].r<<' '<<emojis[i].g<<' '<<emojis[i].b<<'\n';
	}
	struct node first;
	for(int i=0;i<3;i++){first.bounds[i][0]=0.;first.bounds[i][1]=255.;}
	tree.push_back(first);
	propagate(avg_range(first.bounds,0),avg_range(first.bounds,1),avg_range(first.bounds,2),0);
	iterate_print();
	return 0;
}
