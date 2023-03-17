#include <cstdint>
#include <cassert>
#include <iostream>
int f() {
   
   return 42;
}

int main() {
   int i = 7;
   // pointer to integer and back
   std::uintptr_t v1 = reinterpret_cast<std::uintptr_t>(&i); // static_cast is an error
   std::cout << "The value of &i is " << std::showbase << std::hex << v1 << '\n';
   int *p1 = reinterpret_cast<int *>(v1);
   (static_cast<bool>(p1 == &i) ? void(0) : __assert_fail("p1 == &i", "/tmp/__clava_woven_84e42b32-0db1-4994-94ae-3111249a36af_fabiom/src.cpp", 15, __extension__ __PRETTY_FUNCTION__));
   // pointer to function to another and back
   void (*fp1) () = reinterpret_cast<void (*) ()>(f);
   // fp1(); undefined behavior
   int (*fp2) () = reinterpret_cast<int (*) ()>(fp1);
   std::cout << std::dec << fp2() << '\n'; // safe
   // type aliasing through pointer
   char *p2 = reinterpret_cast<char *>(&i);
   std::cout << (p2[0] == '\x7' ? "This system is little-endian\n" : "This system is big-endian\n");
   // type aliasing through reference
   reinterpret_cast<unsigned int &>(i) = 42;
   std::cout << i << '\n';
   __attribute__((unused))
   int const & const_iref = i;
   // int &iref = reinterpret_cast<int&>(
   //     const_iref); // compiler error - can't get rid of const
   // Must use const_cast instead: int &iref = const_cast<int&>(const_iref);
}
