#define ENABLE_WARNING
#ifdef ENABLE_WARNING
  #define WARNING_MSG "Warning: Something might go wrong!"
#else
  #define WARNING_MSG ""
#endif

#define STRINGIFY(x) #x
#define PRAGMA_MESSAGE(x) _Pragma(STRINGIFY(message x))

int main() {
    PRAGMA_MESSAGE("Hello, world!")
    PRAGMA_MESSAGE("This is a C99 program.")
    PRAGMA_MESSAGE(WARNING_MSG)

    return 0;
}

// OR

/*

#define ENABLE_WARNING
#ifdef ENABLE_WARNING
  #define WARNING_MSG "Warning: Something might go wrong!"
#else
  #define WARNING_MSG ""
#endif

int main() {
    _Pragma("message \"Hello, world!\"")
    _Pragma("message \"This is a C99 program.\"")
    _Pragma(WARNING_MSG)

    return 0;
}

*/