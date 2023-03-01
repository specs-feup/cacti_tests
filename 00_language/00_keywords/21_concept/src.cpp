#include <string>
#include <cstddef>
#include <concepts>
 
template<typename T>
concept Hashable = requires(T a)
{
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

template<Hashable T>
void f(T) {}