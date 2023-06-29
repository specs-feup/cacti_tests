#include <iostream>
 
int main()
{
    int i = 2;
    switch (i)
    {
        case 1:
            i++;
        case 2:
        case 3:
        case 5:
        case 6:
            break;
    }
}
