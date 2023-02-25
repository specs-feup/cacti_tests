constexpr int f(); 
constexpr bool b1 = noexcept(f()); // false, undefined constexpr function
constexpr int f() { return 0; }
constexpr bool b2 = noexcept(f()); // true, f() is a constant expression

constexpr unsigned factorial(unsigned n)
{
    return n < 2 ? 1 : n * factorial(n - 1);
}

int main(int argc, const char*[])
{
    constexpr unsigned x{factorial(4)};
    std::cout << x << '\n';
 
    unsigned y = factorial(argc); // OK
}