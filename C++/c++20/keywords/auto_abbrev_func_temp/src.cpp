void f1(auto);                       
void f2(C1 auto);                   
void f3(C2 auto...);                  
void f4(const C3 auto *, C4 auto &);

template <class T, C U>
void g(T x, U y, C auto z); 