template<int N = 0>
void pr43370() {
  int arr[2];
  __atomic_store_n(arr, 0, 5);
}

template<int N = 0>
void foo() {
  int arr[2];
  (void)__atomic_compare_exchange_n(arr, arr, 1, 0, 3, 4);
}

void useage(){
  pr43370();
  foo();
}

int main() {}