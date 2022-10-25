#include <stdio.h>
#include <pthread.h>
#include <math.h>
#include <stdlib.h>


/***** Begin *****/
typedef struct parameter
{
        int low;
        int high;
} parameter;
int a[10000];
int b[10000];

void sort(void *arg){
	parameter *p =(parameter*)arg;
	int high = p->high;
	int low = p->low;
	int i,j;
	int max,temp;
	for (i=high; i>low; --i)
    {
        max = i;
        for (j=i-1; j>=low; --j)
        {
            if (a[j] > a[max])
            {
                max = j;
            }
        }
		temp = a[i];
		a[i] = a[max];
		a[max] = temp;
    }
}

int main()
{
	int n;
	int i,j,index;
	scanf("%d",&n);
	for(i=0;i<n;i++){
		scanf("%d",&a[i]);
	}
	pthread_t p1,p2;
	parameter *par1,*par2;
	par1 = (parameter *)malloc(sizeof(parameter));
	par2 = (parameter *)malloc(sizeof(parameter));
	par1->high = n/2;
	par1->low = 0;
	par2->high = n-1;
	par2->low = n/2+1;
	int ret1 = pthread_create(&p1, NULL, sort, (void *)par1);
	int ret2 = pthread_create(&p2, NULL, sort, (void *)par2);
    if(ret1 != 0|| ret2 != 0){
        printf("Create thread error!\n");
        return -1;
	}
	// sort(a,0,n/2);
	// sort(a,n/2+1,n-1);
	pthread_join(p1, NULL);
	pthread_join(p2, NULL);
	//printf("%d %d",n/2,n/2+1);
	index = 0;
	i = 0;
	j = n/2+1;
	while(i<=n/2 && j<=n-1){  //进行归并
		if(a[i] < a[j]){
			b[index++] = a[i];
			i++;
		}
		else{
			b[index++] = a[j];
			j++;
		}
	}
	if(i > n/2){
		while(j<=n-1){
			b[index++] = a[j];
			j++;
		}
	}
	else{
		while(i<=n/2){
			b[index++] = a[i];
			i++;
		}
	}

	for(i=0;i<n;i++){
		if(i!=n-1) printf("%d ",b[i]);
		else printf("%d",b[i]);
	}
	return 0;
}
/***** End *****/
