#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>
#include <string.h>

/***** Begin *****/
int a[2000];
int a1[1000];
int a2[1000];
int b[2000];
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


int main(int argc, char *argv[])
{
	int numprocs,myid;
	MPI_Status status;
	int param1[3];
	int param2[3];
	int recv_p[3];
	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &myid);
	MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
	if(myid==0){
		int i,j,n;
		scanf("%d",&n);
		for(i=0; i<n; i++){
			scanf("%d",&a[i]);
		}
		if(n>1){
			param1[0] = 0;
			param1[1] = n/2;
			param1[2] = n;
			param2[0] = n/2+1;
			param2[1] = n-1;
			param2[2] = n;
			MPI_Send(param1, 3, MPI_INT, 1, 11, MPI_COMM_WORLD); //发送1号排序参数
			MPI_Send(param2, 3, MPI_INT, 2, 12, MPI_COMM_WORLD); //发送2号排序参数
			MPI_Send(a, n, MPI_INT, 1, 21, MPI_COMM_WORLD); //发送排序数组
			MPI_Send(a, n, MPI_INT, 2, 22, MPI_COMM_WORLD); //发送排序参数

			MPI_Recv(a1, n, MPI_INT, 1, 1, MPI_COMM_WORLD,&status);  //接收1号排序结束
			MPI_Recv(a2, n, MPI_INT, 2, 2, MPI_COMM_WORLD,&status);  //接收2号排序结束
			for(i=0; i<n; i++){
				if(i<=n/2){
					a[i] = a1[i];
				}
				else{
					a[i] = a2[i];
				}
			}
			merg(a,b,0,n/2,n-1);

			for(i=0;i<n;i++){
				if(i!=n-1) printf("%d ",b[i]);
				else printf("%d",b[i]);
			}
		}
		else
			printf("%d",a[0]);
	}
	else if(myid == 1|| myid == 2){
		MPI_Recv(recv_p, 3, MPI_INT, 0, 10+myid, MPI_COMM_WORLD,&status);
		MPI_Recv(a, recv_p[2], MPI_INT, 0, 20+myid, MPI_COMM_WORLD,&status);
		sort(recv_p[0],recv_p[1]);
		MPI_Send(a, recv_p[2], MPI_INT, 0, myid, MPI_COMM_WORLD);
	}
	MPI_Finalize();
	return 0;
}
/***** End *****/
