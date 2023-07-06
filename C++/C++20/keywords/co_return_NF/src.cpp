#include <coroutine>
#include <iostream>
 
struct promise;
 
struct coroutine : std::coroutine_handle<promise>
{
    using promise_type = struct promise;
};
 
struct promise
{
    coroutine get_return_object() { return {coroutine::from_promise(*this)}; }
    std::suspend_always initial_suspend() noexcept { return {}; }
    std::suspend_always final_suspend() noexcept { return {}; }
    void return_void() {}
    void unhandled_exception() {}
};
 
struct S
{
    int i;
    coroutine f()
    {
        std::cout << i;
        co_return;
    }
};
 
void bad1()
{
    coroutine h = S{0}.f();
    h.resume();
    h.destroy();
}
 
coroutine bad2()
{
    S s{0};
    return s.f();
}
 
void bad3()
{
    coroutine h = [i = 0]() -> coroutine
    {
        std::cout << i;
        co_return;
    }();
    h.resume();
    h.destroy();
}
 
void good()
{
    coroutine h = [](int i) -> coroutine
    {
        std::cout << i;
        co_return;
    }(0);
    h.resume();
    h.destroy();
}

int main() {}