class B {
    public:
    typedef int g;
};

class D {
    public:
    typedef int g;
};

template<typename... bases>
struct X : bases...
{
    using typename bases::g...;
};

int main() {}