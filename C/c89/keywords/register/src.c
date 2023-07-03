#include <stdio.h>

int main()
{
    register int counter;
    for (counter = 0; counter < 5; counter++) {
        printf("Counter value: %d\n", counter);
    }
    return 0;
}