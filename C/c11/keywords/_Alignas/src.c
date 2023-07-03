#include <stdalign.h>
#include <stdio.h>
 
// every object of type struct sse_t will be aligned to 16-byte boundary
// (note: needs support for DR 444)
struct sse_t
{
    _Alignas(16) float sse_data[4];
};

// every object of type struct data will be aligned to 128-byte boundary
struct data
{
    char x;
    _Alignas(128) char cacheline[128]; // over-aligned array of char,
                                      // not array of over-aligned chars
};