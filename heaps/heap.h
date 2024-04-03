#include <vector>

template <typename T>
struct heap{
	std::vector<T> tree;
	heap():tree(1){}
	heap(std::vector<T> v):tree(1){
		for(T i:v)push(i);
	}
	int size(){return tree.size()-1;}
	bool empty(){return tree.size()==1;}
	void prop(int i){
		while(i>1){
			if(tree[i]<tree[i>>1]){
				T t=tree[i>>1];
				tree[i>>1]=tree[i];
				tree[i]=t;
				i>>=1;
			}else break;
		}
	}
	T top(){
		return tree[1];
	}
	void push(T v){
		tree.push_back(v);
		prop(tree.size()-1);
	}
	void pop(){
		if(tree.size()==1)return;
		int i=1,s=tree.size();
		while((i<<1)<s){
			if((i<<1|1)<s){
				if(tree[i<<1]<tree[i<<1|1]){
					tree[i]=tree[i<<1];
					i<<=1;
				}else{
					tree[i]=tree[i<<1|1];
					i=i<<1|1;
				}
			}else{
				tree[i]=tree[i<<1];
				i<<=1;
			}
		}
		if(i!=s-1){
			tree[i]=tree[s-1];
			prop(i);
		}
		tree.pop_back();
	}
};
