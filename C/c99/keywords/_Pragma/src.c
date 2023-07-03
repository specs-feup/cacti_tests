#include <stdio.h>

#define ENABLE_WARNING
#ifdef ENABLE_WARNING
  #define WARNING_MSG "Warning: Something might go wrong!"
#else
  #define WARNING_MSG ""
#endif

int main() {
    _Pragma("message \"Hello, world!\"")
    _Pragma("message \"This is a C99 program.\"")
    _Pragma("message \"" WARNING_MSG "\"")

    printf("This is a C99 program.\n");
    return 0;
}