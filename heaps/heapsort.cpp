#include <iostream>
#include "heap.h"
using namespace std;

int main(){
	int n;cin>>n;
	vector<int> v(n);
	for(int i=0;i<n;++i)cin>>v[i];
	heap<int> h(v);
	while(h.size()){
		cout<<h.top()<<' ';
		h.pop();
	}
	cout<<'\n';
}
