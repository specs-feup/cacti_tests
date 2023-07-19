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

JSON_DUMP_INDENTATION = 2


def openForReadingOrCreate(filePath: str):
    """Tries to open the given file for reading. If it doesn't exist creates it. Raises an exception in case the file can't be created

    Attributes:
        filePath (str): path to the file to open or create

    Returns:
        a file object returned by python's open() function

    Raises:
        the exception that open(filePath, mode="x") raises
    """

    try:
        f = open(filePath, "r")
    except:
        try:
            f = open(filePath, "x")
        except Exception as e:
            printError(
                f"Couldn't open {filePath} for reading AND couldn't create it")
            raise e
    return f


def getClangCommand(standard: str | None, filePath: str) -> list[str]:
    """If given a c/c++ standard, returns a call clang command with the --std flag equal to the passed value. If not, returns a generic clang call command.
    The call command tries to parse the given file with suppressed warnings and dumps the ast to the standard output.

    Attributes:
        standard (str | None): if type is string, it will be the argument to the --std flag, otherwise unused
        filePath (str): path to the file that is to be parsed by clang.

    Returns:
        list[str]: the command to execute clang. Can be run using e.g. subprocess.check_output(command)
    """

    if standard == None:
        printWarning(f"running file: {filePath}:  " +
                     " ".join(['clang', '-Xclang', '-ast-dump', '-w', '-S', filePath]))
        return ['clang', '-Xclang', '-ast-dump', '-w', '-S', filePath]
    else:
        printWarning(f"running file: {filePath}:  " + " ".join(
            ['clang', f'--std={standard}', '-Xclang', '-ast-dump', '-w', '-S', filePath]))
        return ['clang', f'--std={standard}', '-Xclang', '-ast-dump', '-w', '-S', filePath]


def getFileExtension(fileName: str) -> str:
    """Returns the file's extension without the dot (.)

    Attributes:
        fileName (str): name of the file with the extension

    Returns:
        str: the given file's extension e.g. cpp    
    """

    return os.path.splitext(fileName)[1][1:]


def printError(message: str) -> None:
    """Prints a message in red to standard output

    Attributes:
        message (str): message to be printed
    """
    
    print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)


def printWarning(message: str) -> None:
    """Prints a message in yellow to standard output

    Attributes:
        message (str): message to be printed
    """

    print(Fore.YELLOW + Style.BRIGHT + message + Style.RESET_ALL)


def handleArgumentParsing() -> argparse.Namespace:
    """Creates an ArgumentParser, adds the necessary arguments and returns the parsed arguments.

    Returns:
        argparse.Namespace: a Namespace object containing all the parsed arguments. Check argparse's documentation for further details
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source', dest="srcPath", required=True,
                        help="path to the tests directory. The directory's structure should abide by cacti's test folder convention.")

    return parser.parse_args()


def getUsedStandard(filepath: str) -> str | None:
    """Tries to find the most specific (further down the directory tree) instance of a directory whose name is a standard recognized by this program. Check the standards global variable declared in this script and the cacti's convention for testing directories structure for more information.

    Attributes:
        filepath (str): path to the source test file whose standard we want to find

    Returns:
        str: the recognized standard's name in lowercase if found
        None: if a recognized standard isn't found in the path
    """

    filepathSections = reversed(filepath.split(path.sep))
    for section in filepathSections:
        if section.lower() in standards:
            return section
    return None


def getPreviousBuildId(jsonObject: dict[str, any]) -> str:
    """Returns the build id in the jsonObject if present, otherwise returns the MISSING_BUILD_ID constant defined in this file. The build id's key is defined as a constant in this file as well.

    Attributes:
        jsonObject (dict[str, any]): the json object to search for the build id

    Returns:
        str: either the build id present in the json object or the MISSING_BUILD_ID constant defined in this file
    """

    if KEY_BUILD_ID not in jsonObject:
        jsonObject[KEY_BUILD_ID] = MISSING_BUILD_ID
    return jsonObject[KEY_BUILD_ID]


def generateNewBuildId() -> str:
    """Generates a new build id based on the current time. The exact format of this build id is dictated by the BUILD_ID_FORMAT constant defined in this file
    
    Returns:
        str: a new build id based on the current time
    """

    now = datetime.now()
    return now.strftime(BUILD_ID_FORMAT)


def createChangesSectionIfNotExists(jsonObject: dict[str, any]) -> None:
    """Looks for the changes' key (defined as a constant in this file) in jsonObject. If it isn't found, initializes it as an empty list

    Attributes:
        jsonObject (dict[str, any]): the json object in which to search for or create the change section
    """

    if KEY_CHANGES not in jsonObject:
        jsonObject[KEY_CHANGES] = []


def getMostRecentChange(jsonObject: dict[str, any]) -> dict[str, int | list[str]] | None:
    """ Returns the most recent change recorded in jsonObject if it exists.

    Attributes:
        jsonObject (dict[str, any]): the json object to search for changes in
    
    Returns
        None: if no changes were recorded in the object
        dict[str, int | list[str]]: the change json object if found
    """

    if len(jsonObject[KEY_CHANGES]) == 0:
        return None
    return sorted(jsonObject[KEY_CHANGES])[-1]


def getPreviousKeywords(jsonObject: dict[str, any]) -> set[str]:
    """Tries to find the nodes listed in jsonObject. If none are found an empty set is returned.

    Attributes:
        jsonObject: the json object to search for the keywords in
    
    Returns:
        set[str]: a set with the found keywords or an empty set if none were found
    """

    if KEY_NODE_LIST not in jsonObject:
        return set()
    return set(jsonObject[KEY_NODE_LIST])


def handleChangesSection(jsonObject: dict[str, any], currentKeywords: set[str], newBuildId: str) -> None:
    """Handles all activities dealing with the changes section, including creating it if it doesn't exist, generating the newest change and updating the changes section accordingly.

    Attributes:
        jsonObject (dict[str, any]): the json object whose changes section we want to update
        currentKeywords (set[str]): a set with the most recent node names generated by clang
        newBuildId (str): the build id that identifies the build during which this change is being executed
    """

    createChangesSectionIfNotExists(jsonObject)

    previousBuildId = getPreviousBuildId(jsonObject)

    previousKeywords: set[str] = getPreviousKeywords(jsonObject)

    newNodes: set[str] = currentKeywords.difference(previousKeywords)
    removedNodes: set[str] = previousKeywords.difference(currentKeywords)
    keptNodes: set[str] = currentKeywords.intersection(previousKeywords)

    newChangeEntry = dict()
    newChangeEntry[KEY_CHANGE_NEXT_ID] = newBuildId
    newChangeEntry[KEY_CHANGE_PREVIOUS_ID] = previousBuildId
    newChangeEntry[KEY_CHANGE_KEPT] = list(keptNodes)
    newChangeEntry[KEY_CHANGE_NEW] = list(newNodes)
    newChangeEntry[KEY_CHANGE_REMOVED] = list(removedNodes)

    jsonObject[KEY_CHANGES].append(newChangeEntry)
    jsonObject[KEY_CHANGES].sort(key=lambda x: x[KEY_CHANGE_NEXT_ID])
    jsonObject[KEY_CHANGES].reverse()


def handleTestName(srcFilePath: str, jsonObject: dict[str, any]) -> str:
    """Returns the test name present in jsonObject if it exists, otherwise searches for it in srcFilePath and updates the jsonObject accordingly.
    
    Attributes:
        srcFilePath (str): the path to a file that is inside the test directory. Can be either src.c(pp) or metadata.json
        jsonObject (dict[str, any]): the json object that potentially contains the test name
    
    Returns:
        str: the name of the test
    """

    if KEY_TEST_NAME not in jsonObject:
        jsonObject[KEY_TEST_NAME] = path.basename(path.dirname(srcFilePath))
    return jsonObject[KEY_TEST_NAME]


def handlePreviousKeywords(jsonObject: dict[str, any]) -> set[str]:
    """Tries to find the nodes listed in jsonObject. If the key (that is defined in this file) isn't found then it's initialized as an empty list.

    Attributes:
        jsonObject (dict[str, any]): the json object to search for node keywords in

    Returns:
        set[str]: the set with the nodes listed in the json object. Is an empty set if none were found.
    
    """

    if KEY_NODE_LIST not in jsonObject:
        jsonObject[KEY_NODE_LIST] = list()
    return set(jsonObject[KEY_NODE_LIST])


def getNodes(srcFilePath: str) -> set[str]:
    """Gets the nodes generated by the given file when parsed by clang using an adequate command (see getClangCommand for further information).
    
    Attributes:
        srcFilePath (str): path to the file that will be parsed by clang

    Returns:
        set[str]: set of the nodes generated by clang when parsing the given file with the appropriate command
    """

    clangCommand = getClangCommand(getUsedStandard(srcFilePath), srcFilePath)
    rawAstText = subprocess.check_output(clangCommand).decode('utf-8')
    newNodes: set[str] = extractKeywords(rawAstText)
    return newNodes


def updateMetadataFile(metadataFilePath: str, jsonContent: dict[str, any], newNodes: set[str], f) -> None:
    """Handles updating a metadata file in case it already exists.
    
    Attributes:
        metadataFilePath (str): path to the metadata file
        jsonContent (dict[str, any]): the json object that is obtained by parsing the given file. Parsing is handled elsewhere for exception catching purposes
        newNodes (set[str]): a set with the names of the nodes generated by clang when parsig the corresponding test file
        f: the metadata file pointer in reading mode
    """

    testName: str = path.basename(path.dirname(metadataFilePath))

    # When test names aren't node names then they won't be in the generated node keywords
    if testName in newNodes:
        newNodes.remove(testName)
    newBuildId = generateNewBuildId()
    handleChangesSection(jsonContent, newNodes, newBuildId)
    jsonContent[KEY_NODE_LIST] = list(newNodes)
    jsonContent[KEY_BUILD_ID] = newBuildId
    f.close()
    try:
        f = open(metadataFilePath, mode="w")
        json.dump(jsonContent, f, indent=JSON_DUMP_INDENTATION)
    except:
        printError(f"Couldn't open {metadataFilePath} for writing.")
        return
    finally:
        f.close()


def createNewMetadataFile(metadataFilePath: str, newNodes: set[str]) -> None:
    """Handles creating a metadata file for a test that doesn't already have one.
    
    Attributes:
        metadataFilePath (str): path to the metadata file
        newNodes (set[str]): a set with the names of the nodes generated by clang when parsig the corresponding test file
    """

    jsonContent = dict()
    handleTestName(metadataFilePath, jsonContent)

    buildId = generateNewBuildId()
    handleChangesSection(jsonContent, newNodes, buildId)
    jsonContent[KEY_BUILD_ID] = buildId
    jsonContent[KEY_NODE_LIST] = list(newNodes)

    try:
        f = open(metadataFilePath, mode="w")
        json.dump(jsonContent, f, indent=JSON_DUMP_INDENTATION)
    except:
        printError(f"Couldn't open {metadataFilePath} for writing.")
        return
    finally:
        f.close()


def generateMetadatas(baseDirectoryPath: str) -> None:
    """Iterates over all nested files within baseDirectoryPath whose extensions are in the lookForExtensions global variable and updates/generates metadata fils for them
    
    Attributes:
        baseDirectoryPath (str): the path to the directory which contains all the test source files. This directory should abide by cacti's test directories convention
    """

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
                f = openForReadingOrCreate(metadataFilePath)
            except Exception as e:
                printError(
                    f"Error while opening {metadataFilePath} for reading: {e}!")
                f.close()
                continue

            try:
                jsonContent: dict[str, any] = json.loads(f.read())
                updateMetadataFile(metadataFilePath, jsonContent, newNodes, f)
                f.close()

            except Exception as e:
                f.close()
                createNewMetadataFile(metadataFilePath, newNodes)



def extractRelevantBlock(lines: list[str], searchString: str) -> list[str]:
    """Looks for the first line with searchString in lines and then returns all lines after that, including that one.
    
    Attributes:
        lines (list[str]): the list of strings from which you want to extract the block
        searchString (str): the string that will be used to define the line threshold

    Returns:
        list[str]: the block of relevant lines
    """
    
    extractedLines = []
    foundStart = False

    for line in lines:
        if searchString in line:
            foundStart = True
        if foundStart:
            extractedLines.append(line)
    return extractedLines


def extractKeywords(output: str) -> set[str]:
    """Given clang's AST dump, finds the block relevant to the test (defined by the commonSrcFilePart defined in this file) and extracts keywords that relate to nodes being tested by cacti

    Attributes:
        output: clang's ast dump as a string

    Returns:
        set[str]: a set with the relevant node names
    """

    fileTranslationUnit = "\n".join(
        extractRelevantBlock(output.split("\n"), commonSrcFilePart))
    keywords = re.findall(
        r'\b\w+(?:Expr|Decl|Operator|Literal|Cleanups|Stmt)\b', fileTranslationUnit)
    return set((keyword[3:] if keyword.find("3") != -1 else keyword) for keyword in keywords)


if __name__ == '__main__':

    args = handleArgumentParsing()
    baseDirectoryPath = path.abspath(path.join(os.getcwd(), args.srcPath))

    if (not os.path.isdir(baseDirectoryPath)):
        printError("Specified path is not a directory!")
        exit()

    generateMetadatas(baseDirectoryPath)
