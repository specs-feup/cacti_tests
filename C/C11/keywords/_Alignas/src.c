struct sse_t
{
    _Alignas(16) float sse_data[4];
};

struct data
{
    char x;
    _Alignas(128) char cacheline[128];
};

int main() {}