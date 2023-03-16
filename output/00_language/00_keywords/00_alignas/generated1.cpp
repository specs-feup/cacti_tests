// every object of type struct_float will be aligned to alignof(float) boundary
// (usually 4):

struct struct_float {
   
} __attribute__((aligned(float))));

// your definition here
// every object of type sse_t will be aligned to 32-byte boundary:

struct sse_t {
   float sse_data[4];
} __attribute__((aligned(32)));

// the array "cacheline" will be aligned to 64-byte boundary:

__attribute__((aligned(64)))
char cacheline[64];