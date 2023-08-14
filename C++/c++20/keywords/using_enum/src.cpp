enum class fruit
{
    orange,
    apple
};

struct S
{
    using enum fruit; 
};

void f()
{
    S s;
    s.orange; 
    S::orange; 
}