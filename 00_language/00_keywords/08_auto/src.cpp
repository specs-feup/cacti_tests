auto LL0 = [] {};
auto LL1 = []() {};
auto LL2 = []() mutable {};
auto LL3 = []() constexpr {};

auto L0 = [] constexpr {};
auto L1 = [] mutable {};
auto L2 = [] noexcept {};
auto L3 = [] constexpr mutable {};
auto L4 = [] mutable constexpr {};
auto L5 = [] constexpr mutable noexcept {};
auto L6 = [s = 1] mutable {};
auto L7 = [s = 1] constexpr mutable noexcept {};
auto L8 = [] -> bool { return true; };
auto L9 = []<typename T> { return true; };
auto L10 = []<typename T> noexcept { return true; };
auto L11 = []<typename T> -> bool { return true; };
auto L12 = [] consteval {};
auto L13 = []() requires true {};
auto L14 = []<auto> requires true() requires true {};
auto L15 = []<auto> requires true noexcept {};
auto L16 = [] [[maybe_unused]]{};


auto XL9 = []() static consteval {};
auto XL10 = []() static constexpr {};

auto XL11 = [] static {};
auto XL12 = []() static {};
