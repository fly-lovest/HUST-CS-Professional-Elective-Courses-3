#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>

/***** Begin *****/
int PT[1000000];
int main()
{
	int n;
	int i,j;
	int index = 0;
	clock_t startTime, endTime;
	scanf("%d",&n);

	// startTime = clock();
	for(i=1; i<=n; i++){
		if(i == 1){
			PT[index] = 1;
			index++;
		}
		else if(i == 2){
			PT[index] = 1;
			index++;
			PT[index] = 1;
			index++;
		}
		else{
			PT[index] = 1;
			index++;
			#pragma omp parallel for 
			for(j=1;j<=i-2;j++){
				PT[index] = PT[index-i] + PT[index-i+1];
				index++;
			}
			PT[index] = 1;
			index++;
		}
	}
	// endTime = clock();
	// printf("并行花费时间：%ld\n",endTime-startTime);

	index = 0;
	printf("[");
	for(i=1;i<=n;i++){
		if(i != n){
			printf("[");
			for(j=1;j<=i;j++){
				if(j!=i)
					printf("%d,",PT[index++]);
				else
					printf("%d",PT[index++]);
			}
			printf("],");
		}
		else{
			printf("[");
			for(j=1;j<=i;j++){
				if(j!=i)
					printf("%d,",PT[index++]);
				else
					printf("%d",PT[index++]);
			}
			printf("]");
		}
	}
	printf("]\n");
	return 0;
}
/***** End *****/
