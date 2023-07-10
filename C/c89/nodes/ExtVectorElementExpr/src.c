typedef float __attribute__((ext_vector_type(3))) float3;

int main(){
    float3 v = (float3){1.0f, 2.0f, 3.0f};
    float y = v.y;
    return 0;
}