int main() {
    void* targets[] = {&&label};
    goto *targets[0];
    label:
    return 0;
}