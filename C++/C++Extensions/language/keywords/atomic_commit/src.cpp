#include <atomic>

int a;

void thread_func() {
    
    atomic_commit
    {
      ++a;          
    }       
}