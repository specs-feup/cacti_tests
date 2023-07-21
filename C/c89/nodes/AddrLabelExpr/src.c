int main() {
    void *label = &&my_label;
my_label:
    return 0;
}