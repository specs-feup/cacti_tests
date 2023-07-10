namespace NamespaceA {
    void functionA();
}

namespace NamespaceB {
    namespace AliasNamespace = NamespaceA;

    void functionB() {
        AliasNamespace::functionA();
    }
}

int main() {
    NamespaceB::functionB();

    return 0;
}
