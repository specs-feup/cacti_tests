#define FEATURE_LEVEL 2

int main() {
    int a;
#if FEATURE_LEVEL == 1
    a = 1;
#endif
}
