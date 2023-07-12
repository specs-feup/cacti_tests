#include <concepts>

template <typename T>
concept Incrementable = requires(T value) {
    { ++value } -> std::convertible_to<T>;
};

int main() {}