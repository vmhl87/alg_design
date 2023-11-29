#include <iostream>
using namespace std;

typedef struct node{
	int v;
	node *next;
} node;

void push(int v){
	node *n=new node();
	n->v=v;n->next=head;
	head=n;
}

int pop(){
	int ret=head->v;
	node *tmp=head->next;
	delete head;
	head=tmp;
	return ret;
}

public class stack{
	node *head;
	stack(){
		
	}
	void push(int v){
		node *n=new node();
		n->v=v;n->next=head;
		head=n;
	}
	int pop(){
		int ret=head->v;
		node *tmp=head->next;
		delete head;head=tmp;
		return ret;
	}
};

int main(){
	stack st=new stack();
	st.push(1);st.push(2);
	cout<<st.pop()<<' '<<st.pop()<<'\n';
	return 0;
}
