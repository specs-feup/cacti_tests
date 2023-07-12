//adapted from: https://www.geeksforgeeks.org/const_cast-in-c-type-casting-operators/

int main () {
    const int value = 10;
    const int *ptr = &value;
    int *ptr1 = const_cast<int *>(ptr);
    return 0;
}