void f(int n, int * restrict p, int * restrict q)
{
    while (n-- > 0)
        *p++ = *q++;
}
 
int main(void)
{
    int d[100] = {0};
    f(50, d + 50, d);
}