void foo() {
    while (true)
    {
    int i = 1;
    continue;
    i = 2;
    }

    do
    {
        int i = 1;
        continue;
        i = 2;
    } while (true);

    for (int tmp=1;tmp<2;tmp++)
    {
        int i = 1;
        continue;
        i = 2;
    }
    
    for (int j = 0; 2 != j; ++j)
    {
        for (int k = 0; k < 5; k++)     // only this loop is affected by continue
        {
            if (k == 3)
                continue;
            // this statement is skipped each time k == 3:
            std::cout << '(' << j << ',' << k << ") ";
        }
    }
}