void f(int n, int * restrict p, int * restrict q)
{
    while (n-- > 0)
        *p++ = *q++; // none of the objects modified through *p is the same
                     // as any of the objects read through *q
                     // compiler free to optimize, vectorize, page map, etc.
}
 
void g(void)
{
    extern int d[100];
    f(50, d + 50, d); // OK
    f(50, d + 1, d);  // Undefined behavior: d[1] is accessed through both p and q in f
}