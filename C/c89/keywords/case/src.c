#include <stdio.h>
 
int main(void)
{
    int i = 2;
    switch (i) {
        case 1: printf("1");
        case 2: printf("2");   // i==2, so execution starts at this case label
        case 3: printf("3");
        case 4:
        case 5: printf("45");
                break;         // execution of subsequent cases is terminated
        case 6: printf("6");
    }
}