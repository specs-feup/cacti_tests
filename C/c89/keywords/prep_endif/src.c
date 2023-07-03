#include <stdio.h>

#define FEATURE_LEVEL 2

int main() {
#if FEATURE_LEVEL == 1
    printf("Feature level 1\n");
#elif FEATURE_LEVEL == 2
    printf("Feature level 2\n");
#else
    printf("Unknown feature level\n");
#endif
    return 0;
}
