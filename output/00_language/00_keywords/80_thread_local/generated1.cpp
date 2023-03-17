template <class T>
struct S {
   static int tlm;
};
int S::tlm = 0; // "static" does not appear here