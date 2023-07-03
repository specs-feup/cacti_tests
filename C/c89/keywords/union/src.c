struct v
{
   union // anonymous union
   {
       struct { int i, j; }; // anonymous structure
       struct { long k, l; } w;
   };
   int m;
} v1;
 
v1.i = 2;   // valid