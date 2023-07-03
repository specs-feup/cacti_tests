#define ENABLE_FEATURE

int main(void) {
    int a;
#if defined(ENABLE_FEATURE)
    a = 1;
#else
    a = 2;
#endif
}