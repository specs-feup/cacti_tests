#define ABCD 2
#include <stdio.h>
 
int main(void)
{
 
#ifdef ABCD
    printf("1: yes\n");
#else
    printf("1: no\n");
#endif
}