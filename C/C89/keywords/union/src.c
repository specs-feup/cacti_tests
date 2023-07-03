struct v
{
   union // anonymous union
   {
       struct { int i, j; }; // anonymous structure
       struct { long k, l; } w;
   };
   int m;
} v1;
 
int main() {
    v1.i = 2;    
}