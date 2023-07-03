#include <stdio.h>
 
int main(void) 
{
    for (int i = 0; i < 10; i++) {
        if (i != 5) continue;
        printf("%d ", i);             // this statement is skipped each time i != 5
    }
}