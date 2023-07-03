#include <stdalign.h>

struct sse_t
{
    alignas(16) float sse_data[4];
};
 
struct data
{
    char x;
    alignas(128) char cacheline[128];
};
 
 int main() {}