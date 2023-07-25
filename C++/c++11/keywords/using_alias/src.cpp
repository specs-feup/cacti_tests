template <class T>
struct Alloc
{};

template <class T>
using Vec = vector<T, Alloc<T>>;

Vec<int> v; 