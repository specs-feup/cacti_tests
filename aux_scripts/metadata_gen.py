import sys
import subprocess
import re
import json
import os
from os import path
import argparse
from colorama import Fore, Style ## dependency

lookForExtensions = ["c", "cpp"]
standards = ["c89", "c95", "c99", "c11", "c17", "c++98", "c++11", "c++14", "c++17", "c++20"]
commonSrcFilePart = "src.c"

KEY_CHANGES: str = "changes"

def getClangCommand(standard: str | None, filePath: str) -> list[str]:
    if standard == None:
        return ['clang', '-Xclang', '-ast-dump', '-S', filePath]
    else:
        return ['clang', f'--std={standard}', '-Xclang', '-ast-dump', '-S', filePath]

def getFileExtension(fileName: str) -> str:
    """Returns the file's extension without the dot (.)"""
    return os.path.splitext(fileName)[1][1:]

def printError(message: str) -> None:
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)

def handleArgumentParsing() ->  argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    
    parser.add_argument('-s', '--source', dest="srcPath", required=True, help="path to the tests directory. The directory's structure should abide by cacti's test folder convention.")
    
    return parser.parse_args()

def getUsedStandard(filepath: str):
    filepathSections = reversed(filepath.split(path.sep))
    for section in filepathSections:
        if section.lower() in standards:
            return section
    return None



def updateMetadataFile(srcFilePath: str, jsonContent: dict[str, any], f) -> None:
    clangCommand = getClangCommand(getUsedStandard(srcFilePath), srcFilePath)
    rawAstText = subprocess.check_output(clangCommand).decode('utf-8')
    currentKeywords = extract_keywords(rawAstText)
    # TODO remove test name from current keywords
    previousKeywords = jsonContent
    # TODO finish function

    return

def createNewMetadataFile(srcFilePath: str, f) -> None:
    # TODO
    return

def generateMetadatas(baseDirectoryPath: str) -> None:
    for dirpath, _, files in os.walk(baseDirectoryPath):
        for fileName in files:
            if getFileExtension(fileName) not in lookForExtensions: continue
            srcFilePath = path.join(dirpath, fileName)
            metadataFilePath = path.join(dirpath, "metadata.json")
            
            try:
                f = open(metadataFilePath)
            except:
                printError(f"Error while opening {metadataFilePath}!")
                f.close()
                continue
            
            try:
                jsonContent: dict[str, any] = json.loads(f.read())
                updateMetadataFile(srcFilePath, jsonContent, f)
            except:
                createNewMetadataFile(srcFilePath, f)
            finally:
                f.close()



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

def extract_keywords(output: str):
    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), commonSrcFilePart))
    keywords = re.findall(r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
    return set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)


# directory -> either C or C++
def execute_clang(directory):
    language = directory.lower()
    standard_list = os.listdir(directory)
    standard_list = [standard for standard in standard_list if "extensions" not in standard.lower() and "23" not in standard]
        
    # Iterate over all standards
    for standard in standard_list:
        standard_path = os.path.join(directory, standard)
        print("standard_path: " + standard_path)
        # Getting the standard name
        standard_match = re.search(r'([^\\/]+)$', standard_path)
        standard_name = standard_match.group(1)

        # List of keywords and nodes folders
        folder_list = os.listdir(standard_path)
        
        # Iterate over all folders
        for folder in folder_list:
            folder_path = os.path.join(standard_path, folder)
            print("folder_path: " + folder_path)
            keyNodes = os.listdir(folder_path)

            for keyNode in keyNodes:
                keyNode_path = os.path.join(folder_path, keyNode)
                print("keyNode_path: " + keyNode_path)
                # List of files
                src_file_list = os.listdir(keyNode_path)
                
                # Iterate over all files
                for src_file in src_file_list:
                    src_file_path = os.path.join(keyNode_path, src_file)
                    print("file_path: " + src_file_path)
                    command = ['clang', f'--std={standard_name}', '-Xclang', '-ast-dump', '-S', src_file_path]
                    output = subprocess.check_output(command).decode('utf-8')
                    source_string = "src.c" if language == "C" else "src.cpp"
                    print("source " + source_string)
                    file_translation_unit = "\n".join(extract_indentation_block(output.split("\n"), source_string))
                    keywords = re.findall(r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
                    keywords = set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)
                    sorted_keywords = json.dumps(sorted(keywords), indent=4)

                    # Save keywords to "keywords.txt" file
                    with open(os.path.join(keyNode_path, "keywords.txt"), "w") as file:
                        file.write(sorted_keywords)

if __name__ == '__main__':

    args = handleArgumentParsing()
    baseDirectoryPath = path.abspath(path.join(os.getcwd(), args.srcPath()))
    
    if (not os.path.isdir(baseDirectoryPath)):
        printError("Specified path is not a directory!")
        exit()
    
    generateMetadatas(baseDirectoryPath)
