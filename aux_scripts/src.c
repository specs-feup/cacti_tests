struct MyStruct{};

struct MyStruct foo(){
    struct MyStruct obj;
    return obj;
}

int main(){
    foo();
}
