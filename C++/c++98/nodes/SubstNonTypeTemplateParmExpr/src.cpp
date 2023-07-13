#include <iostream>

template <int N>
void printValue() {
    std::cout << "The value is: " << N << std::endl;
}

int main() {
    printValue<42>();
    return 0;
}