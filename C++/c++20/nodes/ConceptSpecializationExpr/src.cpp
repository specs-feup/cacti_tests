#include <concepts>

template <typename T>
concept Integral = std::is_integral_v<T>;

int main() {
    bool isInt = Integral<int>;
    return 0;
}