#include <assert.h> // no longer needed since C23
 
int main(void)
{
    _Static_assert(1 == 1,
                  "Whoa dude, you knew!");
}