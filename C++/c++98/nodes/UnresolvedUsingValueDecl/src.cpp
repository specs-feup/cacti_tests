template <class T>
class Base {
    void foo();
};

template <class T>
class A : public Base<T> {
  using Base<T>::foo;
};

int main() {}