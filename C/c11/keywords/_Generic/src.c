#define Square(X) _Generic((X), \
                int: square_int, \
                float: square_float, \
                default: square_default \
                )(X)

void square_int(int x) {
    int result = x * x;
}

void square_float(float x) {
    float result = x * x;
}

void square_default() {
}

int main(void) {
    int num_int = 5;
    float num_float = 3.14;

    Square(num_int);
    Square(num_float);

    return 0;
}