//adpated from: https://stackoverflow.com/questions/59918247/calling-an-operator-function-in-a-class-in-c

class MyClass {       
  public:              
    MyClass();
    int operator()(unsigned char* C1, unsigned char* C2){};
};

int main() {
  MyClass myObj;    
  unsigned char s1[] = "Hello";
  unsigned char s2[] = "World";
  myObj(s1, s2);
  return 0;
}