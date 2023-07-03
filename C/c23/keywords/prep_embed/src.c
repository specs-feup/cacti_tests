const unsigned char null_terminated_file_data[] = {
    #embed "might_be_empty.txt" \
        prefix(0xEF, 0xBB, 0xBF, ) /* UTF-8 BOM */ \
        suffix(,)
    0 // always null-terminated
};