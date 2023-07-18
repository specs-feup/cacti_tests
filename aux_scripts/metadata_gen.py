import sys
import subprocess
import re
import json
import os

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



# directory -> either C or C++
def execute_clang(directory):
    language = "C++" if directory == "C++" else "C"
    standard_list = os.listdir(directory)
    
    # Iterate over all standards
    for standard in standard_list:
        standard_path = os.path.join(directory, standard)

        # Getting the standard name
        standard_match = re.search(r'([^\\/]+)$', standard_path)
        standard_name = standard_match.group(1)

        # List of keywords and nodes folders
        folder_list = os.listdir(standard_path)
        
        # Iterate over all folders
        for folder in folder_list:
            folder_path = os.path.join(standard_path, folder)

            keyNodes = os.listdir(folder_path)

            for keyNode in keyNodes:
                keyNode_path = os.path.join(folder_path, keyNode)
                # List of files
                src_file_list = os.listdir(folder_path)
                
                # Iterate over all files
                for src_file in src_file_list:
                    src_file_path = os.path.join(folder_path, src_file)
                    command = ['clang', f'--std={standard_name}', '-Xclang', '-ast-dump', '-S', src_file_path]
                    output = subprocess.check_output(command).decode('utf-8')
                    source_string = "src.c" if language == "C" else "src.cpp"
                    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), source_string))
                    keywords = re.findall(r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
                    keywords = set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)
                    sorted_keywords = json.dumps(sorted(keywords), indent=4)

                    # Save keywords to "keywords.txt" file
                    with open(os.path.join(folder_path, "keywords.txt"), "w") as file:
                        file.write(sorted_keywords)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py <directory>')
        sys.exit(1)

    directory = sys.argv[1]

    execute_clang(directory)
