#include <iostream>
using namespace std;

void quick_sort(int start, int end, int* arr){
	int pivot=(start+end)/2;
	
}

void display_arr(int arr[], int len){
	int i=0;
	while(i<len)cout<<arr[i++]<<' ';
	cout<<'\n';
	for(int i=0;i<15;i++){
		for(int j=0;j<25;j++)if(15-i-1<(arr[j]*6)/10)cout<<'#';else cout<<' ';
		cout<<'\n';
	}
}

int main(){
	int arr[25];
	for(int i=0;i<25;i++) arr[i]=rand()%25;
	display_arr(arr,25);
	quick_sort(0, 24, arr);
	display_arr(arr,25);
	return 0;
}
