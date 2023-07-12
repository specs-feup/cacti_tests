typedef int v4si __attribute__((vector_size(16)));
int main(){
    v4si v = (v4si){1,2,3,4};
    return 0;
}