struct MyStruct {
    int operator()() {
        return 1;
    }
};

int main(){
    MyStruct obj;
    int result = obj();
    return 0;
    
}