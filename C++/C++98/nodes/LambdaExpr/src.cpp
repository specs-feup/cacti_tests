int main() {
    int multiplier = 2;

    auto lambda = [multiplier](int x) {
        return x * multiplier;
    };
}