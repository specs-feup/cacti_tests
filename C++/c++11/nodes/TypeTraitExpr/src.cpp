#include <type_traits>

int main() {
    __is_pod(int) == true;
    return 0;
}