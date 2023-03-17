#include <iostream>

struct Object {
   // non-trivial destructor
   ~Object() noexcept {
      std::cout << "d";
   }
};


struct Trivial { // trivial ctor and dtor
   double d1;
   double d2;
};
int main() {
   int a = 10;
   // loop using goto
   label:
   Object obj;
   std::cout << a << " ";
   a = a - 2;
   if(a != 0) {
      goto label; // jumps out of scope of obj, calls obj destructor
   }
   std::cout << '\n';
   // goto can be used to efficiently leave a multi-level (nested) loops
   for(int x = 0; x < 3; x++) {
      for(int y = 0; y < 3; y++) {
         std::cout << '(' << x << ',' << y << ") " << '\n';
         if(x + y >= 3) goto endloop;
      }
   }
   endloop:
   std::cout << '\n';
   goto label2; // jumps into the scope of n and t
   __attribute__((unused))
   int n; // no initializer
   __attribute__((unused))
   Trivial t; // trivial ctor/dtor, no initializer
   label2:
   {
      Object obj3;
      goto label3; // jumps forward, out of scope of obj3
   }
   label3:
   std::cout << '\n';
}
