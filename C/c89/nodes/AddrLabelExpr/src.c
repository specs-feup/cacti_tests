int main(){
    void* label = &&my_label;
    goto *label;

my_label:
    return 0;
}