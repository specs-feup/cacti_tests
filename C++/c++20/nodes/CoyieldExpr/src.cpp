#include <coroutine>
 
template <typename T>
struct Generator
{
    struct promise_type;
    using handle_type = std::coroutine_handle<promise_type>;
 
    struct promise_type {
 
        Generator get_return_object() {
            return Generator(handle_type::from_promise(*this));
        }
        
        std::suspend_always initial_suspend() { return {}; }
        
        std::suspend_always final_suspend() noexcept { return {}; }
        
        void unhandled_exception() {}
 
        template <std::convertible_to<T> From>
        std::suspend_always yield_value(From&& from) {
            return {};
        }
    };
 
    handle_type h_;
 
    Generator(handle_type h)
        : h_(h)
    {}
};
 
Generator<int>
foo() {
    co_yield 1;
}
 
int main() {}