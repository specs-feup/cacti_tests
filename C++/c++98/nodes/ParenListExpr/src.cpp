template <typename T>
struct Generator
{
    struct MyStruct{};
 
    MyStruct h_;
 
    Generator(MyStruct h)
        : h_(h)
    {}
}; 
 
int main() {}