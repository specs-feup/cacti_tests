template<class T>
concept C = requires
{
    new int[-(int)sizeof(T)];
};

int main() {}