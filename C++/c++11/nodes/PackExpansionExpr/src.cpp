template<typename F, typename ...Types>
void forward(F f, Types &&...args) {
  f(static_cast<Types&&>(args)...);
}