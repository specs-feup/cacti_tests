struct Linear {
  double a, b;

  double operator()(double x) const { return a * x + b; }
};