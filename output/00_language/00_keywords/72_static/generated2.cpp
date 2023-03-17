#include <iostream>
#include <string>
using namespace std;
void demo() {
   static int count = 0;
   cout << count << " ";
   count++;
}

int main() {
   for(int i = 0; i < 5; i++)
      demo();
   
   return 0;
}
