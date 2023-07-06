class T {
  int x;

  void foo() {
    x = 6;       // same as this->x = 6;
    this->x = 5; // explicit use of this->
  }
};