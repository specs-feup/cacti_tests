#include <stdio.h>

extern const double pi;

int main() {
    printf("The value of pi is: %lf\n", pi);
    return 0;
}
const double pi = 3.14159;