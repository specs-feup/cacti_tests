int main() {

  switch (0) {
  case 1:
    break;
  default:
    // compilation error: jump to default:
    // would enter the scope of 'x' without initializing it
    break;
  }
}