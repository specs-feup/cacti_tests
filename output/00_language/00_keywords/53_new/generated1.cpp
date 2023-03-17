#include <cstdio>
#include <cstdlib>
#include <new>
// no inline, required by [replacement.functions]/3
__attribute__((visibility("default")))
void * operator new(std::size_t sz) {
   std::printf("1) new(size_t), size = %zu\n", sz);
   if(sz == 0) ++sz; // avoid std::malloc(0) which may return nullptr on success
   if(void *ptr = std::malloc(sz)) return ptr;
   throw {}; // required by [new.delete.single]/3
}

// no inline, required by [replacement.functions]/3
__attribute__((visibility("default")))
void * operator new[](std::size_t sz) {
   std::printf("2) new[](size_t), size = %zu\n", sz);
   if(sz == 0) ++sz; // avoid std::malloc(0) which may return nullptr on success
   if(void *ptr = std::malloc(sz)) return ptr;
   throw {}; // required by [new.delete.single]/3
}

__attribute__((visibility("default")))
void operator delete(void *ptr) noexcept {
   std::puts("3) delete(void*)");
   std::free(ptr);
}

void operator delete(void *ptr, std::size_t size) noexcept {
   std::printf("4) delete(void*, size_t), size = %zu\n", size);
   std::free(ptr);
}

__attribute__((visibility("default")))
void operator delete[](void *ptr) noexcept {
   std::puts("5) delete[](void* ptr)");
   std::free(ptr);
}

void operator delete[](void *ptr, std::size_t size) noexcept {
   std::printf("6) delete[](void*, size_t), size = %zu\n", size);
   std::free(ptr);
}

int main() {
   int *p1 = new int;
   delete p1;
   int *p2 = new int[10]; // guaranteed to call the replacement in C++11
   delete[] p2;
}
