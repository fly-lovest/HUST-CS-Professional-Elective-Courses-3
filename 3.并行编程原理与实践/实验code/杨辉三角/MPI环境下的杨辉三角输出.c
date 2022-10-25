#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>
#include <string.h>
#include <time.h>


/***** Begin *****/
int PT[100000];
int main(int argc, char *argv[])
{
	int numprocs,myid;
	MPI_Status status;
	int addend[2];
	int recv_addend[2];
	int sum;
	clock_t startTime, endTime;
	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &myid);
	MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
	if(myid==0){ //0号进程进行放数操作
		int index = 0;
		int i,j,n;
		scanf("%d",&n);

		// startTime = clock();
		for(i=1; i<=n; i++){
			if(i == 1){
				PT[index++] = 1;
			}
			else if(i == 2){
				PT[index++] = 1;
				PT[index++] = 1;
			}
			else{
				PT[index++] = 1;
				int nowindex = index;
				for(j=1;j<=i-2;j++){
					addend[0] = PT[index-i];
					addend[1] = PT[index-i+1];
					MPI_Send(addend, 2, MPI_INT, j%(numprocs-1)+1, j, MPI_COMM_WORLD); //发送加数
					//PT[index] = PT[index-i] + PT[index-i+1];
					index++;
				}
				index = nowindex;
				for(j=1; j<=i-2;j++){
					MPI_Recv(&sum, 1, MPI_INT, j%(numprocs-1)+1, j, MPI_COMM_WORLD,&status);  //接收和数
					PT[index] = sum;
					index++;
				}
				PT[index++] = 1;
			}
		}
		for(i = 1; i < numprocs; i++)
        {
            MPI_Send(addend, 2, MPI_INT, i, 0, MPI_COMM_WORLD);  //发送停止计算信号
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
	}
	else{ //其他进程进行加法计算
		while(1){
			MPI_Recv(recv_addend, 2, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD,&status);
			if(status.MPI_TAG != 0){  //没有接收到停止信号
				sum = recv_addend[0] + recv_addend[1];
				MPI_Send(&sum, 1, MPI_INT, 0, status.MPI_TAG, MPI_COMM_WORLD);
			}
			else{
				break;
			}
		}
	}
	MPI_Finalize();
	return 0;
}
/***** End *****/
