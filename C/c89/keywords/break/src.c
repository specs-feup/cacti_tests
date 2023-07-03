 int main(void)
{
    for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 5; k++) { // only this loop is exited by break
            if (k == 2) break;
        }
    }  
}