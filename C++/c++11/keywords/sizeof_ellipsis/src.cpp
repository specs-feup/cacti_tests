template <typename... Ts>
constexpr auto make_array(Ts &&...ts)
{
    using CT = std::common_type_t<Ts...>;
    return std::array<CT, sizeof...(Ts)>{std::forward<CT>(ts)...};
}