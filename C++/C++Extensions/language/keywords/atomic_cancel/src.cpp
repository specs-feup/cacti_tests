int a;

void thread_func() {
    
    atomic_cancel
    {
      ++a;          
    }       
}
