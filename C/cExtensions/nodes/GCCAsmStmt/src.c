/*
    Code adapted from: https://www.codeproject.com/Articles/15971/Using-Inline-Assembly-in-C-C
*/

int main() {
    int no = 100, val ;
    asm ("movl %1, %%ebx;"
         "movl %%ebx, %0;"
         : "=r" ( val )
         : "r" ( no )
        );
}