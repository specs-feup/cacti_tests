#include <string>
long double operator ""_w(long double);
std::string operator ""_w(const char16_t*, size_t);
unsigned    operator ""_w(const char*);
 
int main()
{
    1.2_w;
    u"one"_w; 
    12_w;     
}