constexpr const char *f(bool p) { return p ? "constant initializer" : g(); }
constinit const char *c = f(true);
