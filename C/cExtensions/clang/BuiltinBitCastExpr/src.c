int main(){
    unsigned int v = 2;
    float floatV = __builtin_bit_cast(float, v);
    return 0;
}