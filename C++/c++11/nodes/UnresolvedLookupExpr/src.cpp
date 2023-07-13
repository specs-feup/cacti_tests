void printArgs(int arg1, double arg2, const char* arg3) {
}

template <typename... Args>
void printNonTemplateArgs(Args... args) {
    printArgs(args...);
}