#include <coroutine>

struct MyCoroutine {
    struct promise_type {
        MyCoroutine get_return_object() {
            return MyCoroutine{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        void return_void() {}

        void unhandled_exception() {}
    };

    std::coroutine_handle<promise_type> coroutine_handle;

    explicit MyCoroutine(std::coroutine_handle<promise_type> handle)
        : coroutine_handle(handle) {}

    ~MyCoroutine() {
        if (coroutine_handle) {
            coroutine_handle.destroy();
        }
    }

    void resume() {
        coroutine_handle.resume();
    }
};

MyCoroutine createCoroutine() {
    co_await std::suspend_always{};
}

int main() {
    MyCoroutine coroutine = createCoroutine();
    coroutine.resume();
    return 0;
}
