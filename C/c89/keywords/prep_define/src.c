#define FUNCTION(name, a) int fun_##name(int x) { return (a) * x; }
 
FUNCTION(quadruple, 4)
FUNCTION(double, 2)

int main() {
    int a = fun_quadruple(1);
    int b = fun_double(2);
}