#include <algorithm>
#include <vector>
#include <iostream>
 
struct Sum
{
    int sum = 0;
    void operator()(int n) { sum += n; }
};
 
int main()
{
    std::vector<int> v = {1, 2, 3, 4, 5};
    Sum s = std::for_each(v.begin(), v.end(), Sum());
    std::cout << "The sum is " << s.sum << '\n';
}