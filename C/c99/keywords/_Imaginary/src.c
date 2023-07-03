#include <complex.h>
#include <stdio.h>
 
int main(void)
{
    double _Imaginary z = 3*I;
    z = 1 / z;
    printf("1/(3.0i) = %+.1fi\n", cimag(z));
}