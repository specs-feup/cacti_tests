int main() {
  const int i = 2;
  switch (i) {
  case 1:
  case 2: // execution starts at this case label
  case 3:
  case 5:
    break; // execution of subsequent statements is terminated
  case 6:
  }
}