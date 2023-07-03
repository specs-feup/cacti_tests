#include <stdlib.h>
#include <stdio.h>
#include <stdnoreturn.h>
 
_Noreturn void exit_now(int i)
{
    exit(i);
}
 
int main(void)
{
    int a = 0;
    exit_now(2);
    a = 1;
}