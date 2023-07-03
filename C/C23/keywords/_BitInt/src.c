typedef _BitInt(K) color;

struct RGB {
    color R;
    color G;
    color B;
}; /* sizeof(RGB) == 3 * K */

int main() {}

// example taken and adapted from https://blog.tal.bi/posts/c23-bitint/
// since https://en.cppreference.com/mwiki/index.php?title=c/keyword/_BitInt&action=edit&redlink=1
// on today's date, is currently unavailable