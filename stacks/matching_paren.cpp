#include <iostream>
#include <string>
using namespace std;

typedef struct node{
	short type;
	node *next;
} node;

node *head;
int len=0;

void push(short h){
	node *tmp=head;
	head=new node();
	head->type=h;
	head->next=tmp;
	len++;
}

short pop(){
	if(len==0)return 0;
	short tmp=head->type;
	node *ptr=head->next;
	delete head;
	head=ptr;
	len--;
	return tmp;
}

void flush(){
	while(pop()){}
	len=0;
}

bool paren_match(string s){
	flush();
	for(char c:s){
		if(c=='(')push(1);
		else if(c==')')if(pop()!=1)return 0;
		else if(c=='[')push(2);
		else if(c==']')if(pop()!=2)return 0;
	}
	if(len)return 0;
	return 1;
}

int main(){
	string s="e";
	while(s!="exit"){
		cin>>s;
		if(paren_match(s))cout<<"parentheses match\n";
		else cout<<"parentheses do not match\n";
	}
}
