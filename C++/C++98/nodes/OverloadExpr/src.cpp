void foo(int i) {}

int main() {
    auto fn = foo;
    fn(2);
    return 0;
}
