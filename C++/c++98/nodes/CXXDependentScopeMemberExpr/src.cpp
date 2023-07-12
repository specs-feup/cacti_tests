template <typename T>
struct Foo {
    Foo () {
        const int x = 42;
        T::Frob (x);
    }
};

int main () {
    return 0;
}