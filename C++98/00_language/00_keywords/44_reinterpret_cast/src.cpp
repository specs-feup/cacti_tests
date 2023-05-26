#include <cassert>
#include <cstdint>

int main() {
  int i = 7;
  int *v = reinterpret_cast<int *>(&i);
}