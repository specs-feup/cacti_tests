template<int N>
void foo() {
    int result = N * 2;
}

int main() {
    foo<42>();
    return 0;
}