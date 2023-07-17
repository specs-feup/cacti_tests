#include <coroutine>
#include <thread>

struct task
{
    bool await_ready() { return false; }
    std::jthread *p_out;
    void await_suspend(std::coroutine_handle<> h)
    {}
    void await_resume() {};
    struct promise_type
    {
        task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };
};

task foo()
{
    co_await task{};
}

int main()
{
    foo();
    return 0;
}