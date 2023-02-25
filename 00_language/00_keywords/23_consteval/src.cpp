consteval int sqr(int n)
{
    return n*n;
}
constexpr int r = sqr(100); // OK
 
int x = 100;
 
consteval int sqrsqr(int n)
{
    return sqr(sqr(n));     // Not a constant expression at this point, but OK
}
 
consteval int f() { return 42; }
consteval auto g() { return &f; }
consteval int h(int (*p)() = g()) { return p(); }
constexpr int r = h();  // OK

#include <iostream>
 
// This function might be evaluated at compile-time, if the input
// is known at compile-time. Otherwise, it is executed at run-time.
constexpr unsigned factorial(unsigned n)
{
    return n < 2 ? 1 : n * factorial(n - 1);
}
 
// With consteval we enforce that the function will be evaluated at compile-time.
consteval unsigned combination(unsigned m, unsigned n)
{
    return factorial(n) / factorial(m) / factorial(n - m);
}
 
static_assert(factorial(6) == 720);
static_assert(combination(4, 8) == 70);
 