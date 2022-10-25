#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>

/***** Begin *****/
//使用选择排序
int a[2000];
int b[2000];
int c[2000];
void sort(int low, int high){
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

void merg(int *source_arr, int *dest_arr, int low, int mid, int high){ //将[low,...,mid]和[mid+1,...,high]进行归并排序
	// i = 0;
	// j = n/2+1;
	int index = low;
	int i = low;
	int j = mid+1;
	while(i<=mid && j<=high){  //进行归并
		if(source_arr[i] < source_arr[j]){
			dest_arr[index++] = source_arr[i];
			i++;
		}
		else{
			dest_arr[index++] = source_arr[j];
			j++;
		}
	}
	if(i > mid){
		while(j<=high){
			dest_arr[index++] = source_arr[j];
			j++;
		}
	}
	else{
		while(i<=mid){
			dest_arr[index++] = source_arr[i];
			i++;
		}
	}
}

int main()
{
	int n;
	int i,j;
	int temp;
	int max;
	clock_t startTime, endTime;
	scanf("%d",&n);
	for(i=0;i<n;i++){
		scanf("%d",&a[i]);
	}

	// startTime = clock();
	#pragma omp parallel sections
	{
		#pragma omp section
			sort(0,n/4);
		#pragma omp section
			sort(n/4+1,n/2);
		#pragma omp section
			sort(n/2+1,n*3/4);
		#pragma omp section
			sort(n*3/4+1,n-1);
	}
	#pragma omp parallel sections  
	{
		#pragma omp section
			merg(a,b,0,n/4,n/2);
		#pragma omp section
			merg(a,b,n/2+1,n*3/4,n-1);
	}
	merg(b,c,0,n/2,n-1);

	//Time = CLOCKS_PER_SEC;
	//printf("%ld\n",Time);
	// endTime = clock();
	// printf("并行花费时间：%ld\n",endTime-startTime);

	// startTime = clock();
	// #pragma omp parallel sections  
	// {
	// 	#pragma omp section
	// 		sort(0,n/2);
	// 	#pragma omp section
	// 		sort(n/2+1,n-1);
	// }
	// merg(a,b,0,n/2,n-1);
	// endTime = clock();
	// printf("并行花费时间：%ld\n",endTime-startTime);

	// startTime = clock();
	// sort(0,n-1);
	// endTime = clock();
	// printf("串行花费时间：%ld\n",endTime-startTime);

	for(i=0;i<n;i++){
		if(i!=n-1) printf("%d ",c[i]);
		else printf("%d",c[i]);
	}
	return 0;
}
/***** End *****/
