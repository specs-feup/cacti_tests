#include <iostream>

int main() {
  int i = 3;
  const int &rci = i;
  const_cast<int &>(rci) = 4;
}
