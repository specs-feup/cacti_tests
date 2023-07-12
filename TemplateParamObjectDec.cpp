struct A
{
    friend bool operator==(const A&, const A&) = default;
};
 
template<A a>
void f()
{
    &a;                       // OK
    const A& ra = a, &rb = a; // Both bound to the same template parameter object
}

int main() {
}