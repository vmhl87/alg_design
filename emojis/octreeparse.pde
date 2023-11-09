import java.io.File;

// struct (c-style) representing emoji color,id
class e{
	float[] val;
	e(color c){
		val=new float[3];
		val[0]=red(c);
		val[1]=green(c);
		val[2]=blue(c);
	}
}

// dynamic arr of emojis; it must be declared globally, so we make it dynamically sized
ArrayList<e> emojis;

// struct representing node in tree
class node{
	// v = split value, l = left index, r = right index
	float v;
	int l;  // also used in ending vals for emoji id
	int r;
	boolean end=false; // self explanatory
	// metadata used for forward propagation
	float[][] bounds;
	boolean finished;
	int rgb;
	node(){
		bounds=new float[3][2];
		finished=false;
	}
}

// dynamic tree
ArrayList<node> tree;

// utility to find if color is within bounds:
//   bounds is defined by { {red_min, red_max}, {green_min, green_max}, {blue_min, blue_max} }
//   and colors are exclusive on lower bound but inclusive on upper bound
boolean in_bounds(float[][] bounds,float[] val){
	for(int i=0;i<3;i++)if(val[i]<=bounds[i][0]||val[i]>bounds[i][1])return false;
	return true;
}

// forward propagate from id
void prop(int id){
	// some of these we do not need to compute
	if(tree.get(id).finished||tree.get(id).end)return;
	// find which color to split on (octree.pde explains this further in depth)
	int rgb=tree.get(id).rgb;
	// compute average of such color property
	float avg=0.,total=0.;
	// foreach etc etc
	for(e e:emojis)
		// we only consider emojis inside our bounds of course
		if(in_bounds(tree.get(id).bounds,e.val)){
			avg+=e.val[rgb];
			total+=1.;
		}
	avg/=total;
	// set split value of this node
	tree.get(id).v=avg;
	// count the # of emojis above and below average value; inefficient but works
	int[] counts={0,0};
	for(e e:emojis)
		if(in_bounds(tree.get(id).bounds,e.val)){
			if(e.val[rgb]>avg)counts[1]++;
			else counts[0]++;
		}
	// push new elements to tree:
	int h=tree.size();
	// set left and right indexes
	tree.get(id).l=h;tree.get(id).r=h+1;
	// allocate new nodes for left,right
	node tmp1=new node(),tmp2=new node();
	// if there is only 1 emoji left of average, add an ending node with that emoji
	if(counts[0]==1){
		// fallback in case something goes very wrong
		tmp1.l=0;
		// find emoji in bounds
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree.get(id).bounds,emojis.get(id).val)&&emojis.get(id).val[rgb]<=avg){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	// if left side is empty, find the first emoji that is in the outer bounds and make ending node
	}else if(counts[0]==0){
		// basically the same
		tmp1.l=0;
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree.get(id).bounds,emojis.get(id).val)){
				tmp1.l=i;break;
			}
		tmp1.end=true;
		tmp1.finished=true;
	// otherwise: push a split node with updated bounds
	}else{
		// first set all bounds equal
		for(int i=0;i<3;i++)for(int j=0;j<2;j++)tmp1.bounds[i][j]=tree.get(id).bounds[i][j];
		// this is a bit complicated but it works
		tmp1.bounds[rgb][1]=avg;
		// advance rgb selector
		tmp1.rgb=(tree.get(id).rgb+1)%3;
		// IMPORTANT: check if there are repeated emojis
		boolean dup=true;float only=-1.;
		// loop through emojis etc etc
		for(e e:emojis){
			if(!in_bounds(tree.get(id).bounds,e.val)||e.val[rgb]>avg)continue;
			if(only<0.)only=e.val[rgb];
			else if(only!=e.val[rgb])dup=false;
		}
		// if only duplicates: fallback to end node
		if(avg==tree.get(id).bounds[rgb][0]||avg==0.||dup){
			tmp1.l=0;
			for(int i=0;i<emojis.size();i++)
				if(in_bounds(tree.get(id).bounds,emojis.get(id).val)){
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
			if(in_bounds(tree.get(id).bounds,emojis.get(id).val)&&emojis.get(id).val[rgb]>avg){
				tmp2.l=i;break;
			}
		tmp2.end=true;
		tmp2.finished=true;
	}else if(counts[1]==0){
		tmp2.l=0;
		for(int i=0;i<emojis.size();i++)
			if(in_bounds(tree.get(id).bounds,emojis.get(id).val)){
				tmp2.l=i;break;
			}
		tmp2.end=true;
		tmp2.finished=true;
	}else{
		for(int i=0;i<3;i++)for(int j=0;j<2;j++)tmp2.bounds[i][j]=tree.get(id).bounds[i][j];
		tmp2.bounds[rgb][0]=avg;
		tmp2.bounds[rgb][1]=tree.get(id).bounds[rgb][1];
		tmp2.rgb=(tree.get(id).rgb+1)%3;
		boolean dup=true;float only=-1.;
		for(e e:emojis){
			if(!in_bounds(tree.get(id).bounds,e.val)||e.val[rgb]<=avg)continue;
			if(only<0.)only=e.val[rgb];
			else if(only!=e.val[rgb])dup=false;
		}
		if(avg==tree.get(id).bounds[rgb][1]||avg==255.||dup){
			tmp2.l=0;
			for(int i=0;i<emojis.size();i++)
				if(in_bounds(tree.get(id).bounds,emojis.get(id).val)){
					tmp2.l=i;break;
				}
			tmp2.end=true;
			tmp2.finished=true;
		}
	}
	// append both sides to tree
	tree.add(tmp1);
	tree.add(tmp2);
	// hopefully this node is finished
	tree.get(id).finished=true;
}

void dump(String finename){
	PrintWriter cout = createWriter(filename);
	cout.println(tree.size());
	for(node n:tree){
		if(n.end){
			cout.print("e "+n.l);
		}else{
			cout.print("n "+n.v+' '+n.l+' '+n.r);
		}
		cout.println();
	}
	cout.flush();cout.close();
}

void dump(){
	dump("octree_dumped.txt");
}

void createOctree(color[] inArr){
	emojis = new ArrayList<e>();
	tree = new ArrayList<node>();
	for(color c:inArr){
		emojis.add(new e(c));
	}
	node first=new node();
	for(int i=0;i<3;i++){first.bounds[i][0]=-1.;first.bounds[i][1]=256.;}
	first.rgb=0;
	tree.add(first);
	int id=0;
	while(id<tree.size()){
		prop(id);
		id++;
	}
	dump();
}
