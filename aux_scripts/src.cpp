#include <iostream>

struct MyClass {
    void myFunction(int x) {
        std::cout << "myFunction(int): " << x << std::endl;
    }

    void myFunction(double x) {
        std::cout << "myFunction(double): " << x << std::endl;
    }
};

int main() {
    MyClass obj;
    obj.myFunction(42); // Member access expression with overloaded functions
    obj.myFunction(3.14);
    return 0;
}
