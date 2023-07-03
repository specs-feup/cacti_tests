#define ABCD 2
#include <stdio.h>
 
int main(void)
{
 
#ifndef ABCD
    printf("1: no\n");
#else
    printf("1: yes\n");
#endif
}