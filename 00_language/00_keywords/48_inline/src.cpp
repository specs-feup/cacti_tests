inline int sum(int a, int b)
{
    return a + b;
}

namespace Lib
{
  inline namespace Lib_1
  {
    template <typename T> class A; 
  }
 
  template <typename T> void g(T) { /* ... */ }
}