template <typename T>
struct X {
    static const int value = 42;
};

template <typename T>
void printValue() {
    int x = X<T>::value;
}

int main() {}