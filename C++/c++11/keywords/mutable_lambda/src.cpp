template <class F>
auto foo(F &&fun)
{
    return [callback = std::forward<F>(fun)](auto &&...args) mutable
    {
        std::invoke(callback, std::forward<decltype(args)>(args)...);
    };
}
