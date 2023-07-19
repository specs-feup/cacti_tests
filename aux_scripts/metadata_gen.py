import subprocess
from datetime import datetime
import re
import json
import os
from os import path
import argparse
from colorama import Fore, Style  # dependency

lookForExtensions = ["c", "cpp"]
standards = ["c89", "c95", "c99", "c11", "c17",
             "c++98", "c++11", "c++14", "c++17", "c++20"]
commonSrcFilePart = "src.c"

KEY_CHANGES: str = "changes"
KEY_NODE_LIST: str = "extraNodes"
KEY_BUILD_ID: str = "buildId"

KEY_CHANGE_PREVIOUS_ID = "previousId"
KEY_CHANGE_NEXT_ID = "nextId"
KEY_CHANGE_KEPT = "kept"
KEY_CHANGE_NEW = "new"
KEY_CHANGE_REMOVED = "removed"
KEY_TEST_NAME = "testName"

BUILD_ID_FORMAT = "%Y%m%d-%H-%M"
# If this missing build id starts with 0 it will always be sorted chronologically to be the first
MISSING_BUILD_ID: str = "0NOID"


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


def handleArgumentParsing() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source', dest="srcPath", required=True,
                        help="path to the tests directory. The directory's structure should abide by cacti's test folder convention.")

    return parser.parse_args()


def getUsedStandard(filepath: str):
    filepathSections = reversed(filepath.split(path.sep))
    for section in filepathSections:
        if section.lower() in standards:
            return section
    return None


def getPreviousBuildId(jsonObject: dict[str, any]) -> str:
    if KEY_BUILD_ID not in jsonObject:
        jsonObject[KEY_BUILD_ID] = MISSING_BUILD_ID
    return jsonObject[KEY_BUILD_ID]


def generateNewBuildId() -> str:
    now = datetime.now()
    return now.strftime(BUILD_ID_FORMAT)


def createChangesSectionIfNotExists(jsonObject: dict[str, any]) -> None:
    if KEY_CHANGES not in jsonObject:
        jsonObject[KEY_CHANGES] = []


def getMostRecentChange(jsonObject: dict[str, any]) -> dict[str, int | list[str]] | None:
    if len(jsonObject[KEY_CHANGES]) == 0:
        return None
    return sorted(jsonObject[KEY_CHANGES])[-1]


def getPreviousKeywords(jsonObject: dict[str, any]) -> set[str]:
    if KEY_NODE_LIST not in jsonObject:
        return set()
    return set(jsonObject[KEY_NODE_LIST])


def handleChangesSection(jsonObject: dict[str, any], currentKeywords: set[str], newBuildId: str) -> None:
    createChangesSectionIfNotExists(jsonObject)

    previousBuildId = getPreviousBuildId(jsonObject)

    previousKeywords: set[str] = getPreviousKeywords()

    newNodes: set[str] = currentKeywords.difference(previousKeywords)
    removedNodes: set[str] = previousKeywords.difference(currentKeywords)
    keptNodes: set[str] = currentKeywords.intersection(previousKeywords)

    newChangeEntry = dict()
    newChangeEntry[KEY_CHANGE_PREVIOUS_ID] = previousBuildId
    newChangeEntry[KEY_CHANGE_NEXT_ID] = newBuildId
    newChangeEntry[KEY_CHANGE_KEPT] = list(keptNodes)
    newChangeEntry[KEY_CHANGE_NEW] = list(newNodes)
    newChangeEntry[KEY_CHANGE_REMOVED] = list(removedNodes)


def handleTestName(srcFilePath: str, jsonObject: dict[str, any]) -> str:
    if KEY_TEST_NAME not in jsonObject:
        jsonObject[KEY_TEST_NAME] = path.dirname(srcFilePath)
    return jsonObject[KEY_TEST_NAME]


def handlePreviousKeywords(jsonObject: dict[str, any]) -> set[str]:
    if KEY_NODE_LIST not in jsonObject:
        jsonObject[KEY_NODE_LIST] = list()
    return set(jsonObject[KEY_NODE_LIST])


def getNodes(srcFilePath):
    clangCommand = getClangCommand(getUsedStandard(srcFilePath), srcFilePath)
    rawAstText = subprocess.check_output(clangCommand).decode('utf-8')
    newNodes: set[str] = extractKeywords(rawAstText)
    return newNodes


def updateMetadataFile(srcFilePath: str, jsonContent: dict[str, any], newNodes: set[str], f) -> None:
    testName: str = path.dirname(srcFilePath)

    # When test names aren't node names then they won't be in the generated node keywords
    if testName in newNodes:
        newNodes.remove(testName)

    newBuildId = generateNewBuildId()
    handleChangesSection(jsonContent, newNodes, newBuildId)
    jsonContent[KEY_NODE_LIST] = list(newNodes)
    jsonContent[KEY_BUILD_ID] = newBuildId
    json.dump(jsonContent, f)


def createNewMetadataFile(srcFilePath: str, newNodes: set[str], f) -> None:
    jsonContent = dict()
    handleTestName(srcFilePath, jsonContent)

    buildId = generateNewBuildId()
    handleChangesSection(jsonContent, newNodes, buildId)
    jsonContent[KEY_BUILD_ID] = buildId
    jsonContent[KEY_NODE_LIST] = list(newNodes)

    json.dump(jsonContent, f)


def generateMetadatas(baseDirectoryPath: str) -> None:
    for dirpath, _, files in os.walk(baseDirectoryPath):
        for fileName in files:
            if getFileExtension(fileName) not in lookForExtensions:
                continue
            srcFilePath = path.join(dirpath, fileName)
            metadataFilePath = path.join(dirpath, "metadata.json")

            try:
                newNodes = getNodes(srcFilePath)
            except Exception as e:
                printError(
                    f"Error while parsing {srcFilePath} with clang: {str(e)}")
                continue

            try:
                f = open(metadataFilePath)
            except:
                printError(f"Error while opening {metadataFilePath}!")
                f.close()
                continue

            try:
                jsonContent: dict[str, any] = json.loads(f.read())
                updateMetadataFile(srcFilePath, jsonContent, newNodes, f)
            except:
                createNewMetadataFile(srcFilePath, newNodes, f)
            finally:
                f.close()


def extractIndentationBlock(lines: list[str], search_string: str) -> list[str]:
    extracted_lines = []
    found_start = False

    for line in lines:
        if search_string in line:
            found_start = True
        if (found_start):
            extracted_lines.append(line)
    print("\n".join(extracted_lines))
    return extracted_lines


def extractKeywords(output: str) -> set[str]:
    file_translation_unit = "\n".join(
        extractIndentationBlock(output.split("\n"), commonSrcFilePart))
    keywords = re.findall(
        r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
    return set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)


# directory -> either C or C++
def executeClang(directory):
    language = directory.lower()
    standard_list = os.listdir(directory)
    standard_list = [standard for standard in standard_list if "extensions" not in standard.lower(
    ) and "23" not in standard]

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
                    command = [
                        'clang', f'--std={standard_name}', '-Xclang', '-ast-dump', '-S', src_file_path]
                    output = subprocess.check_output(command).decode('utf-8')
                    source_string = "src.c" if language == "C" else "src.cpp"
                    print("source " + source_string)
                    file_translation_unit = "\n".join(
                        extractIndentationBlock(output.split("\n"), source_string))
                    keywords = re.findall(
                        r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', file_translation_unit)
                    keywords = set((keyword[3:] if keyword.find(
                        "3") != -1 else keyword) for keyword in keywords)
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
