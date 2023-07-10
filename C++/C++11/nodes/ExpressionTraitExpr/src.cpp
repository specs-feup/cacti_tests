#include <type_traits>

int main() {
    bool isIntegral = std::is_integral<int>::value;
    return 0;
}