export module foo;

export int f();

module :private;
                
int f()
{
    return 42;
}