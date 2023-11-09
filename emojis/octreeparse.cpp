// imports: input/output, vector(dynamic arr; essentially ArrayList)
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

// struct (c-style) representing emoji color,id
struct e{
	float val[3];
};

// dynamic arr of emojis; it must be declared globally, so we make it dynamically sized
vector<struct e> emojis;

// struct representing node in tree
struct node{
	// v = split value, l = left index, r = right index
	float v;
	int l;  // also used in ending vals for emoji id
	int r;
	bool end=false; // self explanatory
	// metadata used for forward propagation
	float bounds[3][2];
	bool finished=false;
	int rgb;
};

// dynamic tree
vector<struct node> tree;

// utility to find if color is within bounds:
//   bounds is defined by { {red_min, red_max}, {green_min, green_max}, {blue_min, blue_max} }
//   and colors are exclusive on lower bound but inclusive on upper bound
bool in_bounds(float bounds[3][2],float val[3]){
	for(int i=0;i<3;i++)if(val[i]<=bounds[i][0]||val[i]>bounds[i][1])return false;
	return true;
}

// forward propagate from id
void prop(int id){
	// some of these we do not need to compute
	if(tree[id].finished||tree[id].end)return;
	// find which color to split on (octree.pde explains this further in depth)
	int rgb=tree[id].rgb;
	// compute average of such color property
	float avg=0.,total=0.;
	// foreach etc etc
	for(struct e e:emojis)
		// we only consider emojis inside our bounds of course
		if(in_bounds(tree[id].bounds,e.val)){
			avg+=e.val[rgb];
			total+=1.;
		}
	avg/=total;
	// print debug for testing
cout<<"    "<<id<<": avg "<<avg<<" total "<<total;
	// set split value of this node
	tree[id].v=avg;
	// count the # of emojis above and below average value; inefficient but works
	int counts[2]={0,0};
	for(struct e e:emojis)
		if(in_bounds(tree[id].bounds,e.val)){
			if(e.val[rgb]>avg)counts[1]++;
			else counts[0]++;
		}
	// debug
cout<<' '<<counts[0]<<' '<<counts[1]<<'\n';
	// push new elements to tree:
	int h=tree.size();
	// set left and right indexes
	tree[id].l=h;tree[id].r=h+1;
	// allocate new nodes for left,right
	struct node tmp1,tmp2;
	// if there is only 1 emoji left of average, add an ending node with that emoji
	if(counts[0]==1){
		// fallback in case something goes very wrong
		tmp1.l=0;
		// find emoji in bounds
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)&&emojis[i].val[rgb]<=avg){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	// if left side is empty, find the first emoji that is in the outer bounds and make ending node
	}else if(counts[0]==0){
		// basically the same
		tmp1.l=0;
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	// otherwise: push a split node with updated bounds
	}else{
		// first set all bounds equal
		for(int i=0;i<3;i++)for(int j=0;j<2;j++)tmp1.bounds[i][j]=tree[id].bounds[i][j];
		// this is a bit complicated but it works
		tmp1.bounds[rgb][1]=avg;
		// advance rgb selector
		tmp1.rgb=(tree[id].rgb+1)%3;
		// IMPORTANT: check if there are repeated emojis
		bool dup=true;float only=-1.;
		// loop through emojis etc etc
		for(struct e e:emojis){
			if(!in_bounds(tree[id].bounds,e.val)||e.val[rgb]>avg)continue;
			if(only<0.)only=e.val[rgb];
			else if(only!=e.val[rgb])dup=false;
		}
		// if only duplicates: fallback to end node
		if(avg==tree[id].bounds[rgb][0]||avg==0.||dup){
			tmp1.l=0;
			for(int i=0;i<emojis.size();i++)
				if(in_bounds(tree[id].bounds,emojis[i].val)){
					tmp1.l=i;break;
				}
			tmp1.end=true;
			tmp1.finished=true;
		}
	}
	// basically the same, but with right endpoint instead
	if(counts[1]==1){
		tmp2.l=0;
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree[id].bounds,emojis[i].val)&&emojis[i].val[rgb]>avg){
				tmp2.l=i;break;
			}
		tmp2.end=true;
		tmp2.finished=true;
	}else if(counts[1]==0){
		tmp2.l=0;
		for(int i=0;i<emojis.size();i++)
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
			for(int i=0;i<emojis.size();i++)
				if(in_bounds(tree[id].bounds,emojis[i].val)){
					tmp2.l=i;break;
				}
			tmp2.end=true;
			tmp2.finished=true;
		}
	}
	// append both sides to tree
	tree.push_back(tmp1);
	tree.push_back(tmp2);
	// hopefully this node is finished
	tree[id].finished=true;
}

// utility to print out tree
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
	char c;int i=0;
	while(cin>>c){
		struct e tmp;
		for(int j=0;j<3;j++){cin>>tmp.val[j];cin>>c;}
		emojis.push_back(tmp);
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
