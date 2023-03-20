// delete []{ return new int; }(); // parse error
delete ([]{ return new int; })();  // OK
