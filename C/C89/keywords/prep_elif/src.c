#define FEATURE_LEVEL 2

int main() {
    int a;
#if FEATURE_LEVEL == 1
    a = 1;
#elif FEATURE_LEVEL == 2
    a = 2;
#else
    a = -1;
#endif
    return 0;
}
