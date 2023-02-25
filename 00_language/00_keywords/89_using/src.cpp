#include <iostream>

namespace A 
{
  int i;
};
using namespace A;

enum class fruit { orange, apple };

using std::cout;

void f()
{
  using enum fruit;
}
