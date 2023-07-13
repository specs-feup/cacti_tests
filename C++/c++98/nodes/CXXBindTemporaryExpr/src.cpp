struct S
{
    S(){}
    ~S(){}
};

void test(){
    const S &s_ref = S();
}
