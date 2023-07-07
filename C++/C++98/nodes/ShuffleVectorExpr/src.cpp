#include <algorithm>
#include <vector>

int main(){
  std::vector<int> v1;
  std::random_shuffle(v1.begin(), v1.end());
  return 0;
}