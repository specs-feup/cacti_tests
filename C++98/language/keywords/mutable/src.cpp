#include <cstdlib>
 
int main()
{
    const struct
    {
        int n1;
        mutable int n2;
    } x = {0, 0};        // const object with mutable member 
}