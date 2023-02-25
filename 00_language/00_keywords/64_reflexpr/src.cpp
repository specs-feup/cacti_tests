// Reflection TS
#include <experimental/reflect>
template <typename Tp>
constexpr std::string_view nameof() {
 using TpInfo = reflexpr(Tp);
}
