#include <stdalign.h>
#include <stddef.h>
#include <stdio.h>
 
int main(void)
{
    printf("Alignment of char = %zu\n", _Alignof(char));
    printf("Alignment of max_align_t = %zu\n", _Alignof(max_align_t));
    printf("alignof(float[10]) = %zu\n", _Alignof(float[10]));
    printf("alignof(struct{char c; int n;}) = %zu\n",
            _Alignof(struct {char c; int n;}));
}