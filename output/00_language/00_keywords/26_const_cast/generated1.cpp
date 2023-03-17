#include <iostream>
int main() {
   int i = 3;
   int const & rci = i;
   const_cast<int &>(rci) = 4;
}
