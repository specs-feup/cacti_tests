#define ABCD 2
 
int main(void)
{
    int a;
#ifndef ABCD
    a = 1;
#endif
}