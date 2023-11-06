#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

#define lines 2169

struct e{
	float val[3];
	int id;
};

struct e emojis[lines];

struct node{
	// prop
	float v;
	int l;  // also used in ending vals for emoji id
	int r;
	float bounds[3][2];
	bool end=false;
	// meta
	bool finished=false;
	int rgb;
};

vector<struct node> tree;

bool in_bounds(float bounds[3][2],float val[3]){
	for(int i=0;i<3;i++)if(val[i]<=bounds[i][0]||val[i]>bounds[i][1])return false;
	return true;
}

void prop(int id){
	if(tree[id].finished||tree[id].end)return;
	int rgb=tree[id].rgb;
	float avg=0.,total=0.;
	for(struct e e:emojis)
		if(in_bounds(tree[id].bounds,e.val)){
			avg+=e.val[rgb];
			total+=1.;
		}
	avg/=total;
cout<<"    "<<id<<": avg "<<avg<<" total "<<total;
	tree[id].v=avg;
	int counts[2]={0,0};
	for(struct e e:emojis)
		if(in_bounds(tree[id].bounds,e.val)){
			if(e.val[rgb]>avg)counts[1]++;
			else counts[0]++;
		}
cout<<' '<<counts[0]<<' '<<counts[1]<<'\n';
	int h=tree.size();
	tree[id].l=h;tree[id].r=h+1;
	struct node tmp1,tmp2;
	if(counts[0]==1){
		tmp1.l=0;
		for(int i=0;i<lines;i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)&&emojis[i].val[rgb]<=avg){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	}else if(counts[0]==0){
		tmp1.l=0;
		for(int i=0;i<lines;i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	}else{
		for(int i=0;i<3;i++)for(int j=0;j<2;j++)tmp1.bounds[i][j]=tree[id].bounds[i][j];
		tmp1.bounds[rgb][0]=tree[id].bounds[rgb][0];
		tmp1.bounds[rgb][1]=avg;
		tmp1.rgb=(tree[id].rgb+1)%3;
		bool dup=true;float only=-1.;
		for(struct e e:emojis){
			if(!in_bounds(tree[id].bounds,e.val)||e.val[rgb]>avg)continue;
			if(only<0.)only=e.val[rgb];
			else if(only!=e.val[rgb])dup=false;
		}
		if(avg==tree[id].bounds[rgb][0]||avg==0.||dup){
			tmp1.l=0;
			for(int i=0;i<lines;i++)
				if(in_bounds(tree[id].bounds,emojis[i].val)){
					tmp1.l=i;break;
				}
			tmp1.end=true;
			tmp1.finished=true;
		}
	}
	if(counts[1]==1){
		tmp2.l=0;
		for(int i=0;i<lines;i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)&&emojis[i].val[rgb]>avg){
				tmp2.l=i;break;
			}
		tmp2.end=true;
		tmp2.finished=true;
	}else if(counts[1]==0){
		tmp2.l=0;
		for(int i=0;i<lines;i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)){
				tmp2.l=i;break;
			}
		tmp2.end=true;
		tmp2.finished=true;
	}else{
		for(int i=0;i<3;i++)for(int j=0;j<2;j++)tmp2.bounds[i][j]=tree[id].bounds[i][j];
		tmp2.bounds[rgb][0]=avg;
		tmp2.bounds[rgb][1]=tree[id].bounds[rgb][1];
		tmp2.rgb=(tree[id].rgb+1)%3;
		bool dup=true;float only=-1.;
		for(struct e e:emojis){
			if(!in_bounds(tree[id].bounds,e.val)||e.val[rgb]<=avg)continue;
			if(only<0.)only=e.val[rgb];
			else if(only!=e.val[rgb])dup=false;
		}
		if(avg==tree[id].bounds[rgb][1]||avg==255.||dup){
			tmp2.l=0;
			for(int i=0;i<lines;i++)
				if(in_bounds(tree[id].bounds,emojis[i].val)){
					tmp2.l=i;break;
				}
			tmp2.end=true;
			tmp2.finished=true;
		}
	}
	tree.push_back(tmp1);
	tree.push_back(tmp2);
	tree[id].finished=true;
}

void disp(){
	int h=tree.size(),end=0,unres=0,res=0;
	for(int j=0;j<h;j++){
		cout<<j<<": ";
		if(tree[j].end){
			end++;
			cout<<"emoji "<<tree[j].l<<" w color ";
			for(int i=0;i<3;i++)cout<<emojis[tree[j].l].val[i]<<' ';
		}else{
			unres++;
			if(tree[j].finished){
				res++;unres--;
				cout<<"split "<<tree[j].v<<" goto "<<tree[j].l<<' '<<tree[j].r;
			}else cout<<"unresolved";
			cout<<' '<<(tree[j].rgb==0?"red":(tree[j].rgb==1?"green":"blue"))<<" bounds ";
			for(int k=0;k<3;k++){cout<<tree[j].bounds[k][0]<<' '<<tree[j].bounds[k][1]<<' ';}
		}
		cout<<'\n';
	}
	cout<<end<<" ending "<<res<<" resolved "<<unres<<" unresolved\n";
}

void dump(){
	ofstream cout("octree_dumped.txt");
	cout<<tree.size()<<'\n';
	for(struct node n:tree){
		if(n.end){
			cout<<"e "<<n.l;
		}else{
			cout<<"n "<<n.v<<' '<<n.l<<' '<<n.r;
		}
		cout<<'\n';
	}
}

int main(){
	fstream cin("parsed.txt");
	for(int i=0;i<lines;i++){
		char c;cin>>c;
		for(int j=0;j<3;j++){cin>>emojis[i].val[j];cin>>c;}
	}
	/*
	for(int i=0;i<lines;i++){
		cout<<emojis[i].val[0]<<' '<<emojis[i].val[1]<<' '<<emojis[i].val[2]<<'\n';
	}
	*/
	struct node first;
	for(int i=0;i<3;i++){first.bounds[i][0]=-1.;first.bounds[i][1]=256.;}
	first.rgb=0;
	tree.push_back(first);
	int id=0;
	while(id<tree.size()){
		prop(id);
		id++;
	}
	disp();
	dump();
	return 0;
}
