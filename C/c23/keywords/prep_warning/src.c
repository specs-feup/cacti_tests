#if __STDC__ != 1
#  error "Not a standard compliant compiler"
#endif
 
#if __STDC_VERSION__ >= 202311L
#  warning "Using #warning as a standard feature"
#endif
 
#include <stdio.h>
int main (void)
{
    printf("The compiler used conforms to the ISO C Standard !!");
}