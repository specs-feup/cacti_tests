#include <cstdlib>

volatile int n = 0;

class S 
{
  void f() volatile;
};
