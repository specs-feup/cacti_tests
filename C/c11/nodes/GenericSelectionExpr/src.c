int main() {
    int v;
    _Generic(v, double: 1, float: 2, default: 3);
    return 0;
}