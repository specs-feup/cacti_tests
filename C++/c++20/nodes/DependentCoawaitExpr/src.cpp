#include <utility>
#include <coroutine>
#include <chrono>

template <typename Awaitable>
std::suspend_never await_and_print(Awaitable&& awaitable) {
    co_await std::forward<Awaitable>(awaitable);
}

int main() {}
