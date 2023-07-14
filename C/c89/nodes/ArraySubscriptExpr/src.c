int testRValueArraySubscriptExpr(void *bytes) {
  int *p = (int*)&bytes[0];
  return 5/(*p);
}
