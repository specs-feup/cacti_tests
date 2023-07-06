import sys
import subprocess
import re
import os
from functools import reduce

def count_leading_whitespace(string):
    spaces = 0
    found_start = False
    for char in string:
        if found_start:
            if char.isspace():
                spaces += 1
            else:
                break
        else:
            if char.isspace():
                spaces += 1
                found_start = True
    
    return spaces

def extract_indentation_block(lines, search_string):
    extracted_lines = []
    found_start = False
    indentation_level = 0
    
    for line in lines:
        if search_string in line:
            extracted_lines.append(line)

            if not found_start:
                indentation_level = count_leading_whitespace(line)

            found_start = True
            continue

        if found_start and count_leading_whitespace(line) > indentation_level:
            extracted_lines.append(line)
        else:
            indentation_level = 0
            found_start = False

    return extracted_lines

def extract_keywords(file_path, cpp_standard):
    command = ['clang', f'--std={cpp_standard}', '-Xclang', '-ast-dump', '-S', file_path]
    output = subprocess.check_output(command).decode('utf-8')
    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), "keywords/"))
    keywords = re.findall(r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
    return set(keyword[3:] + " " + cpp_standard + " " + file_path for keyword in keywords)

def process_directory(directory_path):
    cpp_standard = os.path.basename(directory_path.lower())

    if cpp_standard.find("extension") != -1:
        cpp_standard = "c++20"

    keywords_set = set()
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.c') or file.endswith('.cpp'):
                file_path = os.path.join(root, file)
                keywords_set.update(extract_keywords(file_path, cpp_standard))

        # Remove subdirectories from the search list
        dirs[:] = [d for d in dirs if not d.startswith(cpp_standard)]

    return keywords_set

def get_children_directories(directory_path):
    directories = []
    entries = os.listdir(directory_path)
    
    for entry in entries:
        entry_path = os.path.join(directory_path, entry)
        if os.path.isdir(entry_path):
            directories.append(entry_path)

    return directories

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py <directory_path>')
        sys.exit(1)

    directory_path = sys.argv[1]

    children_directories = get_children_directories(directory_path)

    sets = list()

    print("searching these directories: " + str(children_directories))

    for dir in children_directories:
        keywords_set = process_directory(dir)
        sets.append(keywords_set)
    
    union_set = reduce(lambda s1, s2: s1 | s2, sets)

    # Sort keywords in alphabetical order
        
    sorted_keywords = sorted(union_set)

    # Print keywords to standard output
    for keyword in sorted_keywords:
        print(keyword)

    # Save keywords to "keywords.txt" file
    with open("keywords.txt", "w") as file:
        file.write("\n".join(sorted_keywords))


    