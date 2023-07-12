class A
{
    public: 
        explicit A(int x) {}
};

class B: public A
{
     using A::A;
};