#include <iostream>
struct sometype
{
    void *operator new(std::size_t) = delete;
    void *operator new[](std::size_t) = delete;
};
