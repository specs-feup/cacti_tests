
class T {
   int x;
   void foo() {
      this->x = 6; // same as this->x = 6;
      this->x = 5; // explicit use of this->
   }
   
   void foo() const {
      //      x = 7; // Error: *this is constant
   }
   
   void foo(int x) {
      this->x = x; // unqualified x refers to the parameter
      // 'this->' required for disambiguation
   }
   
   int y;
   T(int x) : x(x), y(this->x) {
   }
   
   T & operator=(T const & b) {
      this->x = b.x;
      
      return *this; // many overloaded operators return *this
   }
};
