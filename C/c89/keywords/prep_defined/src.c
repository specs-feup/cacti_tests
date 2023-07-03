#include <stdio.h>

#define ENABLE_FEATURE

int main() {
#if defined(ENABLE_FEATURE)
    printf("Feature is enabled!\n");
#else
    printf("Feature is disabled!\n");
#endif

    return 0;
}