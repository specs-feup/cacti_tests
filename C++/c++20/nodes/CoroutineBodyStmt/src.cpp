#include <coroutine>

struct MyCoroutine {
    struct promise_type {
        MyCoroutine get_return_object() {}

        std::suspend_always initial_suspend() {}
        std::suspend_always final_suspend() noexcept {}

        void return_void() {}

        void unhandled_exception() {}
    };

};

MyCoroutine createCoroutine() {
    co_await std::suspend_always{};
}

int main() {
    MyCoroutine coroutine = createCoroutine();
    return 0;
}
