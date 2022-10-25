#include <stdio.h>

/***** Begin *****/
//使用选择排序
int a[10000];
int main()
{
	int n;
	int i,j;
	int temp;
	scanf("%d",&n);
	for(i=0;i<n;i++){
		scanf("%d",&a[i]);
	}

	for (i=n-1; i>0; --i)
    {
        int max = i;
        for (j=i-1; j>=0; --j)
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

	for(i=0;i<n;i++){
		if(i!=n-1) printf("%d ",a[i]);
		else printf("%d",a[i]);
	}
	return 0;
}
/***** End *****/