class Derived{
    public:
        void f(int x);
};

void Derived::f(int a){
    this->f(2);
}