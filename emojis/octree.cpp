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

void propagate(float r,float g,float b,int i){
	int counts[2][2][2];
	for(struct e h:emojis){
		if(in_bounds(h,tree[i].bounds)){
			int i[3]={h.r>r?1:0,h.g>g?1:0,h.b>b?1:0};
			counts[i[0]][i[1]][i[2]]++;
		}
	}
	for(int a=0;a<1;a++)
		for(int b=0;b<1;b++)
			for(int c=0;c<1;c++)
				if(counts[a][b][c]<2){
					int h=tree.size();
					struct node tmp;
					tmp.end=true;
					tmp.finalized=true;
					// write id of emoji to tmp.{r,g,b}
					tree[i].next[a][b][c]=h;
					tree.push_back(tmp);
				}else{
					int h=tree.size();
					struct node tmp;
					// set bounds etc
					tree[i].next[a][b][c]=h;
					tree.push_back(tmp);
				}
	tree[i].r=r;tree[i].g=g;tree[i].b=b;
	tree[i].finalized=true;
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
	return 0;
}
