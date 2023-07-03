
int main() {
    const unsigned char null_terminated_file_data[] = {
        #embed "might_be_empty.txt" \
            prefix(0xEF, 0xBB, 0xBF, ) \
            suffix(,)
        0
    };
}