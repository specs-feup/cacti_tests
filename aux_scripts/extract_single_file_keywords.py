import sys
import subprocess
import re
import json

def extract_indentation_block(lines, search_string):
    extracted_lines = []
    found_start = False
    
    for line in lines:        
        if search_string in line:
            found_start = True
        if (found_start):
            extracted_lines.append(line)
    print("\n".join(extracted_lines))
    return extracted_lines

def extract_keywords(file_path, cpp_standard):
    command = ['clang', f'--std={cpp_standard}', '-Xclang', '-ast-dump', '-S', file_path]
    output = subprocess.check_output(command).decode('utf-8')
    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), "src.c"))
    keywords = re.findall(r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
    return set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python script.py <cpp_standard> <file_path>')
        sys.exit(1)

    cpp_standard = sys.argv[1]
    file_path = sys.argv[2]


    keywords = extract_keywords(file_path, cpp_standard)
        
    sorted_keywords = json.dumps(sorted(keywords), indent=4)

    print(sorted_keywords)
    # Save keywords to "keywords.txt" file
    with open("keywords.txt", "w") as file:
        file.write(sorted_keywords)