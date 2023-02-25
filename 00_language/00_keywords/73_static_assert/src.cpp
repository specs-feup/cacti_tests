#include <iostream>
static_assert(sizeof(void*) == 8, 
"DTAMDL(*LLP64) is not allowed for this module.");
int main()
{
    cout << "Assertion passed. 
    The program didn't produce an error";
    return 0;
}