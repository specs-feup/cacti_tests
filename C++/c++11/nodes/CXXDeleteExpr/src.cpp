int main(){
    delete([]{
        return new int;
    })();
    return 0;
}