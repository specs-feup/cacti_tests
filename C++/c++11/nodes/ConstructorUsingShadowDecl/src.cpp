struct Base { Base(int); };
struct Derived : Base {
   using Base::Base;
};

int main() {}