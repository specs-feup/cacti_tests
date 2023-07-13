//adapted from: https://stackoverflow.com/questions/64130311/what-are-the-breaking-changes-caused-by-rewritten-comparison-operators

struct B {};

struct A
{
    bool operator==(B const&);
};

bool operator==(B const&, A const&);

int main()
{
  B{} == A{};                
}