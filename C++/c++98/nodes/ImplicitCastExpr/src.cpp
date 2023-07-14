class Base { };
class Derived : public Base { };
Derived &&ref();
void f(Derived d) {
  Base& b = d; 
              
  Base&& r = ref(); 
                    
}