const int n = 1; // object of const-qualified type
int* p = (int*)&n;
*p = 2; // undefined behavior