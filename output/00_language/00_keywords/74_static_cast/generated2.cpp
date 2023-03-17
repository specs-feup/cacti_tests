#include <vector>
#include <iostream>

struct B {
   int m = 42;
   char const * hello() const {
      
      return "Hello world, this is B!\n";
   }
};


struct D : B {
   char const * hello() const {
      
      return "Hello world, this is D!\n";
   }
};


enum class E {
   ONE = 1,
   TWO,
   THREE,
};


enum EU {
   ONE = 1,
   TWO,
   THREE,
};

int main() {
   // 1. static downcast
   D d;
   B & br = d; // upcast via implicit conversion
   std::cout << "1) " << br.hello();
   D & another_d = static_cast<D &>(br); // downcast
   std::cout << "1) " << another_d.hello();
   // 2. lvalue to xvalue
   std::vector<int> v0{1, 2, 3};
   std::vector<int> v2 = static_cast<std::vector<int>&&>(v0);
   std::cout << "2) after move, v0.size() = " << v0.size() << '\n';
   // 3. initializing conversion
   int n = static_cast<int>(3.14);
   std::cout << "3) n = " << n << '\n';
   std::vector<int> v = static_cast<std::vector<int>>(10);
   std::cout << "3) v.size() = " << v.size() << '\n';
   // 4. discarded-value expression
   static_cast<void>(v2.size());
   // 5. inverse of implicit conversion
   void *nv = &n;
   int *ni = static_cast<int *>(nv);
   std::cout << "5) *ni = " << *ni << '\n';
   // 6. array-to-pointer followed by upcast
   D a[10];
   __attribute__((unused))
   B *dp = static_cast<B *>(a);
   // 7. scoped enum to int
   E e = E::TWO;
   int two = static_cast<int>(e);
   std::cout << "7) " << two << '\n';
   // 8. int to enum, enum to another enum
   E e2 = static_cast<E>(two);
   __attribute__((unused))
   EU eu = static_cast<EU>(e2);
   // 9. pointer to member upcast
   int D::*pm = &D::m;
   std::cout << "9) " << br.*static_cast<int B::*>(pm) << '\n';
   // 10. void* to any type
   void *voidp = &e;
   __attribute__((unused))
   std::vector<int> *p = static_cast<std::vector<int> *>(voidp);
}
