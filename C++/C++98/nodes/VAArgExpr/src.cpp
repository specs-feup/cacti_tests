#include <cstdarg>

int main()
{
    va_list args;
    int value = 0;
    int result = va_arg(args, int);
    return 0;
}