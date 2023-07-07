template<typename... Args>
void foo(Args... args) {
    int result = sizeof...(args);
}

int main() {
    foo(1, 2, 3);
    return 0;
}
