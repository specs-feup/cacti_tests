#define FUNCTION(name, a) int fun_##name(int x) { return (a) * x; }
 
FUNCTION(quadruple, 4)
FUNCTION(double, 2)
 
#undef FUNCTION

int main() {
    int a = 0;
}