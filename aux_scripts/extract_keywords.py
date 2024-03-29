import sys
import subprocess
import re
import os
from functools import reduce


def count_leading_whitespace(string: str) -> int:
    """Counts the number of leading whitespace characters in a string.

    Attributes:
        string (str): The string to count the leading whitespace characters in.

    Returns:
        int: The number of leading whitespace characters in the string.
    """

    spaces: int = 0
    found_start: bool = False
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


def extract_indentation_block(lines: list[str], search_string: str) -> list[str]:
    """Extracts a block of lines that are indented more than the line containing the search string.

    Attributes:
        lines (list[str]): The lines to extract the indentation block from.
        search_string (str): The string to search for in the lines.

    Returns:
        list[str]: The extracted lines.
    """

    extracted_lines: list[str] = []
    found_start: bool = False
    indentation_level: int = 0

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


def extract_keywords(file_path: str, cpp_standard: str) -> set[str]:
    """Extracts the keywords from a file.

    Attributes:
        file_path (str): The path to the file to extract the keywords from.
        cpp_standard (str): The C/C++ standard to use for the extraction.

    Returns:
        set[str]: The extracted keywords.
    """

    command = ['clang', f'--std={cpp_standard}',
               '-Xclang', '-ast-dump', '-S', file_path]
    output = subprocess.check_output(command).decode('utf-8')
    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), "keywords/") +
                                      extract_indentation_block(output.split("\n"), "nodes/"))
    keywords = re.findall(
        r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)

    return set((keyword if not keyword[:2].isdigit() else keyword[3:]) + " " + cpp_standard + " " + file_path for keyword in keywords)


def process_directory(directory_path: str) -> set[str]:
    """Processes a directory and extracts the keywords from all 
    the files in it.

    Attributes:
        directory_path (str): The path to the directory to process.

    Returns:
        set[str]: The extracted keywords.
    """

    cpp_standard: str = os.path.basename(directory_path.lower())

    keywords_set: set[str] = set()

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.c') or file.endswith('.cpp'):
                file_path: str = os.path.join(root, file)
                keywords_set.update(extract_keywords(file_path, cpp_standard))

        # Remove subdirectories from the search list
        dirs[:] = [d for d in dirs if not d.startswith(cpp_standard)]

    return keywords_set


def get_children_directories(directory_path: str) -> list[str]:
    """Gets the children directories of a directory.

    Attributes:
        directory_path (src): The path to the directory to get the children directories of.

    Returns:
        list[str]: The children directories.
    """

    directories: list[str] = []
    entries: list[str] = os.listdir(directory_path)

    for entry in entries:
        entry_path: str = os.path.join(directory_path, entry)
        if os.path.isdir(entry_path):
            directories.append(entry_path)

    return directories


def getKeywordNodes(filePath: str) -> set[str]:
    """Gets the keyword nodes from a file.

    Attributes:
        filePath (str): The path to the file to get the keyword nodes from.

    Returns:
        set[str]: The keyword nodes.
    """

    keyNodes: set[str] = set()
    f = open(filePath, "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        if "keywords/" in line:
            words = line.split()
            keyNodes.add(words[0])
    return keyNodes


def getNodes(filePath: str) -> set[str]:
    """Gets the nodes from a file.

    Attributes:
        filePath (str): The path to the file to get the nodes from.

    Returns:
        set[str]: The nodes.
    """

    nodes: set[str] = set()
    f = open(filePath, "r")
    lines: list[str] = f.readlines()
    f.close()
    for line in lines:
        if "nodes/" in line:
            words = line.split()
            nodes.add(words[0])
    return nodes


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python extract_keywords.py <directory_path>')
        sys.exit(1)

    directory_path = sys.argv[1]

    children_directories = get_children_directories(directory_path)

    sets = list()

    print("searching these directories: " + str(children_directories))

    for dir in children_directories:
        standards = get_children_directories(dir)
        print("searching these standards: " + str(standards))
        for standard in standards:
            keywords_set = process_directory(standard)
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

    file.close()

    exclusiveKeywords = set()
    filePath = "keywords.txt"
    keyword_nodes = getKeywordNodes(filePath)
    nodes = getNodes(filePath)
    exclusiveKeywords = keyword_nodes.difference(nodes)
    f = open("exclusive_keywords.txt", "w+")
    for keyword in exclusiveKeywords:
        f.write(keyword + "\n")
    f.close()
    print(exclusiveKeywords)
