#include <stdio.h>
#include <stdlib.h>
enum { SIZE = 8 };
int main(void)
{
    // trivial example
    int array[SIZE], n = 0;
    do array[n++] = rand() % 2; // the loop body is a single expression statement
    while(n < SIZE);
    puts("Array filled!");
    n = 0;
    do { // the loop body is a compound statement
        printf("%d ", array[n]);
        ++n;
    } while (n < SIZE);
}