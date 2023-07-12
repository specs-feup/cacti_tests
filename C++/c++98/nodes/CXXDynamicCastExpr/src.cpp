//adapted from: https://www.geeksforgeeks.org/dynamic-_cast-in-cpp/

class Base {
    void print(){}
};

class Derived1 : public Base {
    void print(){}
};
 
class Derived2 : public Base {
    void print(){}
};
int main () {
    Derived1 d1;
    Base* bp = dynamic_cast<Base*>(&d1);

    return 0;
}