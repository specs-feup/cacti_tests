#include <assert.h> // no longer needed since C23
 
int main(void)
{
    // Test if math works.
    _Static_assert((2 + 2) % 3 == 1, // or _Static_assert(...
                  "Whoa dude, you knew!");
 
    // This will produce an error at compile time.
    _Static_assert(sizeof(int) < sizeof(char),
                 "this program requires that int is less than char");
}