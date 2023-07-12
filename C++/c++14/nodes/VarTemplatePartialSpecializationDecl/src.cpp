template <int x, int y>
constexpr int foo = -1;

template <>
constexpr float foo<1, 0> = 1.0;

template <int x>
constexpr double foo<1, x> = 1.1;

int main() {}