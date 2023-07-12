void may_throw();

int main(){
  noexcept(may_throw());
  return 0;
}