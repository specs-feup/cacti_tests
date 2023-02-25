#include <iostream>

extern "C"
{
    int open(const char *pathname, int flags); // C function declaration
}
 
extern "C" void f1(void(*pf)()); // declares a function f1 with C linkage,
                             // which returns void and takes a pointer to a C function
                             // which returns void and takes no parameters
 
extern "C" typedef void FUNC(); // declares FUNC as a C function type that returns void
                                // and takes no parameters
 
FUNC f2;            // the name f2 has C++ linkage, but its type is C function
extern "C" FUNC f3; // the name f3 has C linkage and its type is C function void()
void (*pf2)(FUNC*); // the name pf2 has C++ linkage, and its type is
                    // "pointer to a C++ function which returns void and takes one
                    // argument of type 'pointer to the C function which returns void
                    // and takes no parameters'"
 
extern "C"
{
    static void f4(); // the name of the function f4 has internal linkage (no language)
                      // but the function's type has C language linkage
}

int main()
{
    int fd = open("test.txt", 0); // calls a C function from a C++ program
}
 
// This C++ function can be called from C code
extern "C" void handler(int)
{
    std::cout << "Callback invoked\n"; // It can use C++
}

extern "C"
{
    class X
    {
        void mf();           // the function mf and its type have C++ language linkage
        void mf2(void(*)()); // the function mf2 has C++ language linkage;
                             // the parameter has type “pointer to C function”
    };
}

namespace A
{
    extern "C" int f();
}
 
namespace B
{
    extern "C" int f();   // A::f and B::f refer to the same function f with C linkage
}
 
int A::f() { return 98; } // definition for that function

namespace A
{
    extern "C" int h();
}
 
extern "C" int h() { return 97; } // definition for the C linkage function h
                                  // A::h and ::h refer to the same function

template<typename T>
struct A { struct B; };
 
extern "C"
{
    template<typename T>
    struct A<T>::B
    {
        friend void f(B*) requires true {} // C language linkage ignored
    };
}
 
namespace Q
{
    extern "C" void f(); // not ill-formed 
}