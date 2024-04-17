#include <stdio.h>
#define M 1000000000

// multiply vector by matrix (assumed 2x2)
void vmul(long long *v,long long *m){
	long long r1=((*m)*(*v)+(*(m+1))*(*(v+1)))%M,
		r2=((*(m+2))*(*v)+(*(m+3))*(*(v+1)))%M;
	*v=r1,*(v+1)=r2;
}

// multiply 2x2 matrix by itself
void mmul(long long *m){
	long long r1=((*m)*(*m)+(*(m+1))*(*(m+2)))%M,
		 r2=((*m)*(*(m+1))+(*(m+1))*(*(m+3)))%M,
		 r3=((*(m+2))*(*m)+(*(m+3))*(*(m+2)))%M,
		 r4=((*(m+2))*(*(m+1))+(*(m+3))*(*(m+3)))%M;
	*m=r1,*(m+1)=r2,*(m+2)=r3,*(m+3)=r4;
}

int main(){
	long long v[2]={0,1},
		 m[4]={1,1,1,2};
	long long n;
	printf("Enter n: \033[1m");
	scanf("%d",&n);
	long long x=n>>1;
	while(x){
		if(x&1)vmul(v,m);
		mmul(m);
		x>>=1;
	}
	printf("\033[0mFibbonacci number \033[1m%d\033[0m is ",n);
	printf("\033[1m%d\033[0m",*(v+(n&1)));
	if(*(v+(n&1))>99999999)printf(" (truncated to last 9 digits)");
	printf("\n");
}
