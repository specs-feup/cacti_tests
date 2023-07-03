int main(void)
{
    int a = a;
    for (int x = 0; x < 3; x++) {
        for (int y = 0; y < 3; y++) {
            a = a + 1;
            if (x + y == 3) goto endloop;
        }
    }
endloop:;
}