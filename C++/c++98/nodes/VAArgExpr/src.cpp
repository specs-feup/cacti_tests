#include <cstdarg>

int main()
{
    va_list args;
    int result = va_arg(args, int);
    return 0;
}