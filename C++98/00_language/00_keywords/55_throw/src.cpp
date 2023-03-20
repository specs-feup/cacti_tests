try
{
    std::string("abc").substr(10); // throws std::length_error
}
catch (const std::exception& e)
{
    std::cout << e.what() << '\n';
//  throw e; // copy-initializes a new exception object of type std::exception
    throw;   // rethrows the exception object of type std::length_error
}
