#include <type_traits>

int main(){
    bool result = std::is_integral<int>::value;
    return 0;
}