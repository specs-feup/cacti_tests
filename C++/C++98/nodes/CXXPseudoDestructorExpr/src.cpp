template<typename T>
void destroy(T* ptr) {
  ptr->T::~T();
}

int main(){
    return 0;
}