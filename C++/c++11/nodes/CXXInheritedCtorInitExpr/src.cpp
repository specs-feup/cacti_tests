class MyClass {
public:
    MyClass(int x);
};

class MyClass2 : public MyClass{
    public:
    using MyClass::MyClass;
};

int main() {
    MyClass2 obj(42);
    return 0;
}