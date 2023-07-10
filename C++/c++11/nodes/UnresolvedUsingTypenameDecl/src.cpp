template <typename T>
class Base {
public:
    using foo = T;
};

template <class T> class A : public Base<T> {
  using typename Base<T>::foo;
};

int main() {}
