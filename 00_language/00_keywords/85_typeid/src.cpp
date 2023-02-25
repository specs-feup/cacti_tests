#include <iostream>
#include <string>
#include <typeinfo>
 
int main() {
  int i = 10;
  
  const std::type_info& ti = typeid(i);

  return 0;
}
