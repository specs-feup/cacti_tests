template<typename ...Types>
struct count {
  static const unsigned value = sizeof...(Types);
};
