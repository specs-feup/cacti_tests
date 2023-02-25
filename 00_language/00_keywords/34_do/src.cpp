#include <algorithm>
#include <iostream>
#include <string>
 
int main()
{
    int j = 2;
    do // compound statement is the loop body
    {
        j += 2;
        std::cout << j << " ";
    }
    while (j < 9);
}
