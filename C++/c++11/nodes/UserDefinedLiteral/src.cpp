constexpr long double operator"" _m(long double meters){
  return meters;
}

int main(){
  long double distance = 2.5_m;
  return 0;
}