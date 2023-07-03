#include <stddef.h>
#include <stdio.h>
 
void g(int*)
{
    puts("Function g called");
}

int main(){
    g(nullptr);
    auto cloned_nullptr = nullptr;
}