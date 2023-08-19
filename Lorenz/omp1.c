#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

int main(void)
{
    double x, pi,  a = 0.0, b = 1.0, area = 0.0;
    long long n = 100000000l;
    double subInterval = (b - a)/n;     //Step Size
    
    #pragma omp parallel for reduction(+:area) private(x)
    for(long long i = 1; i < n; i++)
    {
        x = (i + 0.5) * subInterval;
        area = area + 4.0/(1.0 + x * x);
    }
    pi = area * subInterval;
    printf("Pi = %lf", pi);
    return 0;
}