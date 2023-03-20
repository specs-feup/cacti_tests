template<class T>
struct S
{
    thread_local static int tlm;
};
 
template<>
thread_local int S<float>::tlm = 0; // "static" does not appear here
