char * const_cast_test(char const *var) {
   
   return const_cast<char *>(var);
}


struct A {
   virtual ~A() noexcept {
   }
};


struct B : public A {
   
};

struct B * dynamic_cast_test(struct A *a) {
   
   return dynamic_cast<struct B *>(a);
}

char * reinterpret_cast_test() {
   
   return reinterpret_cast<char *>(0xdeadbeef);
}

double static_cast_test(int i) {
   
   return static_cast<double>(i);
}

char postfix_expr_test() {
   
   return reinterpret_cast<char *>(0xdeadbeef)[0];
}
