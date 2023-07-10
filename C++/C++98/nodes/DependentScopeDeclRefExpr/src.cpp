template <typename T>
void foo(T value) {
    value.bar();
}

struct MyStruct {
    void bar() {}
};

int main() {
    MyStruct obj;
    foo(obj);
    return 0;
}
