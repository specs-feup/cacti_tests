inline const char *saddr(void) // the inline definition for use in this file
{
    static const char name[] = "saddr";
    return name;
}
int compare_name(void)
{
    return saddr() == saddr(); // unspecified behavior, one call could be external
}
extern const char *saddr(void); // an external definition is generated, too