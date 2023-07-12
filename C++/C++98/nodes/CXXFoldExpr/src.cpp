template<typename... Args>
bool all(Args... args) { return (... && args); }
 
bool b = all(true, true, true, false);

int main(){
    return 0;
}