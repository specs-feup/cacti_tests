template<class T>
constexpr T clone(const T& t){
  return t;
}

void g(int*){}

int main(){
  g(nullptr);
}