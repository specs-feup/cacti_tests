extern "C" int func();

asm(R"(
.globl func
    .type func, @function
    func:
    .cfi_startproc
    movl $7, %eax
    ret
    .cfi_endproc
)");
 
int main()
{
    int n = func();
    asm ("leal (%0,%0,4),%0"
         : "=r" (n)
         : "0" (n));
 
    asm ("movq $60, %rax\n\t"
         "movq $2,  %rdi\n\t" 
         "syscall");
}
