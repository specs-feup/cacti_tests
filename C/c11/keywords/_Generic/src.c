#include <stdio.h>

#define Square(X) _Generic((X), \
                int: square_int, \
                float: square_float, \
                default: square_default \
                )(X)

void square_int(int x) {
    int result = x * x;
    printf("Square of %d is %d\n", x, result);
}

void square_float(float x) {
    float result = x * x;
    printf("Square of %f is %f\n", x, result);
}

void square_default() {
    printf("Unsupported type for squaring.\n");
}

int main(void) {
    int num_int = 5;
    float num_float = 3.14;
    char num_char = 'A';

    Square(num_int);
    Square(num_float);
    Square(num_char);

    return 0;
}