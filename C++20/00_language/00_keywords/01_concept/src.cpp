#include <string>
#include <cstddef>
#include <concepts>

template<class T, class U>
concept Derived = std::is_base_of<U, T>::value;

int main() {}