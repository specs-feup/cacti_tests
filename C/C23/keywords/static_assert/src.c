#include <assert.h>
 
int main(void)
{
    static_assert(2 + 2 == 4, "2+2 isn't 4");
}