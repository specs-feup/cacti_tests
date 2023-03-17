#include <cstdlib>
int main() {
   int n1 = 0; // non-const object
   int const n2 = 0; // const object
   int const n3 = 0; // const object (same as n2)
   int volatile n4 = 0; // volatile object
   
   const struct {
      int n1;
      mutable int n2;
   } x = {0, 0};
   n1 = 1; // ok, modifiable object
   n4 = 3; // ok, treated as a side-effect
   x.n2 = 4; // ok, mutable member of a const object isn't const
   int const & r1 = n1; // reference to const bound to non-const object
   const_cast<int &>(r1) = 2; // ok, modifies non-const object n1
   int const & r2 = n2; // reference to const bound to const object
}
