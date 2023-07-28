import json
import os
import argparse
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np


standardNameToIndex = {
    "c++98": 1,
    "c++11": 2,
    "c++14": 3,
    "c++17": 4,
    "c++20": 5,
    "c89": 6,
    "c99": 7,
    "c11": 8,
    "c23": 9,
}


class standards(Enum):
    stand_11 = 1
    stand_14 = 2
    stand_17 = 3
    stand_20 = 4
    stand_98 = 5
    extensions = 6
    cstand89 = 7
    cstand99 = 8
    cstand11 = 9
    cstand23 = 10


testPhasesNames: list[str] = ["test_parsing", "test_code_generation",
                              "test_idempotency", "test_correctness"]


class TestDetails:
    """Represents the details of one of the 4 test phases: Parsing, Code Generation, Idempotency or Correctness.
    Attention should be payed in respects to the time and tries attributes, as the idempotency test phase does not posses a "time" attribute and all other test phases do not possess a "tries" attribute.

    Attributes:
        name (string): The name of the test phase (parsing, code generation, idempotency or correctness).
        success (bool): Whether this test phase was successful or not.
        time (int): How many seconds it took the compiler to perform this task. Is -1 if the attribute is not applicable to the test or an error occurred. 
        tries (int): How many iterations it took for the code generation to converge. Is -1 if the attribute is not applicable to the test. 
    """

    def __init__(self, name: str, success: bool, time: int = -1, tries: int = -1):
        self.name: str = name
        self.success: bool = success
        self.time: int = time
        self.tries: int = tries

    def __str__(self):
        return "TestDetails <name = " + self.name + ", success = " + str(self.success) + ", time = " + str(self.time) + ", tries = " + str(self.tries) + ">"

    def __repr__(self):
        return "TestDetails <name = " + self.name + ", success = " + str(self.success) + ", time = " + str(self.time) + ", tries = " + str(self.tries) + ">"


class Test:
    """Represents a Test which includes its name (its parent folder's name as per our convention) and the details of all applicable test phases run.

    Attributes:
        name (str): Name of the test. As per our convention, this is the source file's parent folder's name.
        details (list[TestDetails]): A list containing the details of all applicable test phases that were run for this particular test.
    """

    def __init__(self, name: str, testDetails: list[TestDetails]):
        self.name: str = name
        self.details: list[TestDetails] = testDetails

    def __str__(self):
        return "Test <name = " + self.name + ", test details = " + str(self.details) + ">"

    def __repr__(self):
        return "Test <name = " + self.name + ", test details = " + str(self.details) + ">"


class Standard:
    """Contains all information regarding a standard, which has a name and can contain multiple tests.

    Attributes:
        name (str): The standard's name, i.e. c++11
        tests (list[Test]): A list containing all the tests associated with this standard.
    """

    def __init__(self, name: str, tests: list[Test]):
        self.name: str = name
        self.tests: list[Test] = tests

    def __str__(self):
        return "Standard <name = " + self.name + ", result = " + str(self.tests) + ">"

    def __repr__(self):
        return "Standard <name = " + self.name + ", result = " + str(self.tests) + ">"


trueCounter = 0
falseCounter = 0
unknownCounter = 0


def removeTestPrefix(string: str) -> str:
    """Removes test_ from the given string.

    Attributes:
        string (str): the string to be transformed.
    """

    # remove test_
    reducedString = string[5:]
    latexString = reducedString.replace("_", "\_")
    return latexString


def escapeBackslash(string: str) -> str:
    """Adds a \\ before every underscore so that it is interpreted correctly in LaTeX.
        Attributes:
        string (str): the string to be transformed.
    """

    latexString = string.replace("_", "\_")
    return latexString


def snakeToCamelCase(string: str) -> str:
    """Splits the given string on underscores and returns the equivalent in Camel Case

    Attributes:
        string (str): the string to be converted from snake_case to camelCase.
    """

    words = list(map(lambda x: x.capitalize(), string.split("\_")))
    return "".join(words)


def latexBool(bool: bool) -> str:
    """Converts a boolean value to a String that can be used in LaTeX. The word is colored depending on the boolean value. Also updates global counters of tests passed/failed...

    Attributes:
        bool (bool): the value to be converted.
    """

    if bool is True:
        latexBool = r"\textcolor{green}{True}"
        global trueCounter
        trueCounter += 1
        return latexBool
    elif bool is False:
        latexBool = r"\textcolor{red}{False}"
        global falseCounter
        falseCounter += 1
        return latexBool
    else:
        latexBool = r"N/A"
        global unknownCounter
        unknownCounter += 1
        return latexBool


def getStand(stand: Standard) -> int:
    """Gets the corresponding integer id of a given standard.

    Attributes:
        stand (Standard): the standard to be identified.
    """

    return standardNameToIndex[stand.name]


def processDirectory(generalPath: str) -> tuple[list[Test], list[Standard]]:
    """Searches the directory recursively and generates a list with all the standards and their corresponding tests found.

    Attributes:
        generalPath (str): the path to the source directory. This directory should have as direct children directories whose names are reflective of the C/C++ standard used in the tests inside it.
    """

    # Ensure general path is absolute and minimal
    generalPath = os.path.abspath(generalPath)

    tests: list[Test] = []
    standards: list[Standard] = []
    for item in os.listdir(generalPath):
        itemPath = os.path.join(generalPath, item)
        if os.path.isdir(itemPath):
            if item in standardNameToIndex:  # Checks if the item's name corresponds to a standard
                tests.extend(processDirectory(itemPath)[0])
                tests.sort(key=lambda x: x.name)
                stand = Standard(item, tests)
                tests = []
                standards.append(stand)
            else:
                tests.extend(processDirectory(itemPath)[0])
        elif os.path.isfile(itemPath) and item.endswith('.json'):
            result = processFile(itemPath)
            tests.append(result)
    return (tests, standards)


def processFile(filePath: str) -> Test:
    """ Parses the contents of a results json file and returns the corresponding Test object.

    Attributes:
        filePath (str): the path to the results json file.
    """

    with open(filePath) as json_file:
        parsedJson = json.load(json_file)
        name = ""
        testPhases = []

        for key, _ in parsedJson.items():
            if key == "name":
                name = parsedJson[key]
            elif key == "test_idempotency":
                test = TestDetails(key, parsedJson[key]["success"], tries=len(
                    parsedJson[key]["results"]))
                testPhases.append(test)
            else:
                if parsedJson[key]["success"]:
                    test = TestDetails(
                        key, parsedJson[key]["success"], parsedJson[key]["time"])
                else:
                    test = TestDetails(key, parsedJson[key]["success"])
                testPhases.append(test)

        result = Test(name, testPhases)
        return result


def writeStandardTestResultRow(test: Test, f) -> None:
    """ Writes a row to be used in the Standard section's table with the test's results.

    Attributes:
        test (Test): the object that contains the information about the test result.
        f (file): the file to be written in.
    """

    row = r"\textbf{{\fontsize{10}{12}\selectfont " + \
        escapeBackslash(test.name) + r"}}"
    for details in test.details:
        if (details.tries == -1):
            row += r'& {0}&{1}'.format(details.time if details.time != -1 else 'N/A',
                                       latexBool(details.success))
        else:
            row += r'& {0}&{1}'.format(details.tries,
                                       latexBool(details.success))
    row += r' \\[0.5ex]'
    f.write(row+"\n")


def writeStandards(standards: list[Standard], f, outputFolder) -> None:
    """Writes the Standards section of the LaTeX report. This includes creating and filling the table with the test results for every standard.

    Attributes:
        standards (list[Standard]): list of standards to include in this section.
        f (file): file to write the section to.
    """

    # since the first group of tests in some standards
    # fails on the Parsing, we need to retrieve all the possible tests
    # so the table is correctly formed
    exampleTest, maxNumOfTests = findMostCompleteTestInfo(
        getAllTests(standards))

    for standard in standards:
        f.write(r"\section{" + standard.name + r"}"+"\n")
        f.write(r"\subsection{Tests table}"+"\n")
        # start table with a column for source file's name and 2 columns per test
        f.write(r"\begin{xltabular}{\textwidth}{l")

        for x in range(1, maxNumOfTests + 1):
            f.write("cc")
        f.write(r"}" + "\n"+(r"\toprule")+"\n")

        # Write column with source files' names
        f.write(r"\multicolumn{1}{Y}{}"+"\n")

        # Writing header and creating test result columns witchery
        for details in exampleTest.details:
            f.write(r"& \multicolumn{2}{@{}c}{\textbf{" +
                    "{0}".format(snakeToCamelCase(removeTestPrefix(details.name))) + r"}}")

        f.write(r"\\"+"\n")
        f.write(r"\cmidrule{2-"+str(2*len(exampleTest.details)+1)+r"}")

        for details in exampleTest.details:
            if (details.tries == -1):
                f.write(
                    r"&\multicolumn{1}{@{}c}{Time}&\multicolumn{1}{@{}c}{Success}")
            else:
                f.write(
                    r"&\multicolumn{1}{@{}c}{Tries}&\multicolumn{1}{@{}c}{Success}")
        f.write(r"\\"+"\n")
        f.write(r"\midrule"+"\n")
        f.write(r"\endhead")

        # writing result rows
        for test in standard.tests:
            writeStandardTestResultRow(test, f)

        f.write(r"\bottomrule"+"\n")
        f.write(r"\end{xltabular}"+"\n")
        f.write(r"\newpage" + "\n")

        f.write(r"\subsection{Success and Fail Rate chart}"+"\n")
        success, failure = getPercentagesFromStandard(standard)
        x_labels = ["Parsing", "CodeGeneration", "Idempotency", "Correctness"]
        createChart(x_labels, success, failure, "Tests", "Percentage", outputFolder, standard.name)

        f.write(r"\newpage" + "\n")

def getAllTests(standards: list[Standard]) -> list[Test]:
    """Iterates over all the standards and flattens all their tests into a single list.

    Attributes:
        standards (list[Standard]): the list that will be iterated over.
    """

    tests: list[Test] = []
    for standard in standards:
        tests.extend(standard.tests)
    return tests


def findMostCompleteTestInfo(tests: list[Test]) -> tuple[Test, int]:
    """Searches all tests in the list and returns a tuple with the test that includes the highest amount of test phases in its details and the corresponding number of test phases.

    Attributes:
        tests (list[Test]): the list that will be iterated over to search for the most complete test.

    Returns: A tuple with the most complete Test found and the number of test phases present in the test's details.
    """

    exampleTest = None
    maxTestPhases = 0
    for test in tests:
        if (len(test.details) > maxTestPhases):
            maxTestPhases = len(test.details)
            exampleTest = test
    return (exampleTest, maxTestPhases)


def getPTNum(tests: list[Test]) -> float:
    """Calculates the percentage of tests that passed.

    Attributes:
        tests (list[Test]): list of tests to be used to calculate the percentage of tests passed.

    Returns:
        float: percentage of tests passed.
    """
    passedTestPhases: int = 0
    for test in tests:
        for details in test.details:
            if details.success == True:
                passedTestPhases += 1
    return passedTestPhases


def getAbsP(tests: list[Test]) -> float:
    """Calculates the theoretically maximum number of test phases that could be passed, then divides the number of actually passed test phases by that number.
    Counts test phases that weren't run as failed.

    Attributes:
        tests(list[Test]): list of tests to be used to calculate the absolute percentage of tests passed.
    """

    maxPossiblePassedTestPhases: int = len(tests) * len(testPhasesNames)
    passedTestPhases: int = 0
    for test in tests:
        for details in test.details:
            if details.success == True:
                passedTestPhases += 1

    return (passedTestPhases / maxPossiblePassedTestPhases) * 100


def getRelP(tests: list[Test]) -> float:
    """Checks how many test phases succeedeed, how many failed and calculates the percentage based on those two alone.
    Doesn't count with test phases that weren't run.

    Attributes:
        tests (list[Test]): list of tests to be used to calculate the percentage of tests passed.

    Returns:
        float: percentage of tests passed.
    """

    passedTestPhases: int = 0
    failedTestPhases: int = 0
    for test in tests:
        for details in test.details:
            if details.success == True:
                passedTestPhases += 1
            elif details.success == False:
                failedTestPhases += 1
    return (passedTestPhases / (passedTestPhases + failedTestPhases)) * 100


def getTestPhaseTNum(tests: list[Test], testPhaseName: str):
    """ Calculates the number of tests that passed a specific test phase.

    Attributes:
        tests (list[Test]): list of tests to be used to calculate the number of tests passed.
        testPhaseName (str): name of the test phase to be checked.

    Returns:
        int: number of tests that passed the test phase.
    """
    numPassed: int = 0
    for test in tests:
        for details in test.details:
            if details.name == testPhaseName:
                if details.success:
                    numPassed += 1
                break
    return numPassed


def getTestPhaseRelP(tests: list[Test], testPhaseName: str):
    """Calculates the relative percentage of tests that passed a specific test phase.

    Attributes:
        tests (list[Test]): list of tests to be used to calculate the percentage of tests passed.
        testPhaseName (str): name of the test phase to be checked.

    Returns:
        float: percentage of tests passed.
    """
    actualNumTests: int = 0
    numPassed: int = 0
    for test in tests:
        for details in test.details:
            if details.name == testPhaseName:
                actualNumTests += 1
                if details.success:
                    numPassed += 1
                break
    return 100 * numPassed / actualNumTests


def getTestPhaseAbsP(tests: list[Test], testPhaseName: str):
    """Calculates the absolute percentage of tests that passed a specific test phase.

    Attributes:
        tests (list[Test]): list of tests to be used to calculate the percentage of tests passed.
        testPhaseName (str): name of the test phase to be checked.

    Returns:
        float: percentage of tests passed.
    """
    maxNumTests: int = len(tests)
    numPassed: int = 0
    for test in tests:
        for details in test.details:
            if details.name == testPhaseName:
                if details.success:
                    numPassed += 1
                break
    return 100 * numPassed / maxNumTests


def writeTableStart(f, numCols: int):
    """Writes the start of a LaTeX table.

    Attributes:
        f (file): file to be written to.
        numCols (int): number of columns the table will have.
    """
    for _ in range(numCols):
        f.write(r"c|")
    f.write(r" }"+"\n")


def getFirstLatexMultiColumnString(headerNameAndLen: tuple[str, int]):
    """Returns a string that can be used to write a LaTeX table header.

    Attributes:
        headerNameAndLen (tuple[str, int]): tuple containing the name of the header and the 
                                            number of columns it will span.

    Returns:
        str: string that can be used to write a LaTeX table header.
    """
    return r"\multicolumn{" + str(headerNameAndLen[1]) + r"}{|c|}{" + headerNameAndLen[0] + r"}"


def getLatexMultiColumnString(headerNameAndLen: tuple[str, int]):
    """Returns a string that can be used to write a LaTeX table header.

    Attributes:
        headerNameAndLen (tuple[str, int]): tuple containing the name of the header and the 
                                            number of columns it will span.

    Returns:
        str: string that can be used to write a LaTeX table header.
    """
    return r"\multicolumn{" + str(headerNameAndLen[1]) + r"}{c|}{" + headerNameAndLen[0] + r"}"


def writeHeaders(f, multiColHeadersAndLen: list[tuple[str, int]]):
    """Writes the headers of a LaTeX table.

    Attributes:
        f (file): file to be written to.
        multiColHeadersAndLen (list[tuple[str, int]]): list of tuples containing the names of the headers and the number of columns they will span.
    """
    f.write(" & ".join([getFirstLatexMultiColumnString(multiColHeadersAndLen[0])
                        ] + (list(map(getLatexMultiColumnString, multiColHeadersAndLen[1:])))))
    f.write(r" \\"+"\n")


def getSubHeaderString(subHeaders: list[str], headerAndColLen: tuple[str, int]):
    """Returns a string that can be used to write a LaTeX table subheader.

    Attributes:
        subHeaders (list[str]): list of subheaders.
        headerAndColLen (tuple[str, int]): tuple containing the name of the header and the 
                                            number of columns it will span.

    Returns:
        str: string that can be used to write a LaTeX table subheader.
    """
    colLen: int = headerAndColLen[1]
    if colLen == 1:
        return " "
    else:
        return " & ".join(subHeaders[:colLen])


def writeSubHeaders(f, multiColHeadersAndLen: list[tuple[str, int]], subHeaders: list[str]):
    """Writes the subheaders of a LaTeX table.

    Attributes:
        f (file): file to be written to.
        multiColHeadersAndLen (list[tuple[str, int]]): list of tuples containing the names of the headers and the number of columns they will span.
        subHeaders (list[str]): list of subheaders.
    """
    f.write(" & ".join(map(lambda x: getSubHeaderString(
        subHeaders, x), multiColHeadersAndLen)))
    f.write(r" \\" + "\n")


def writeTableResults(f, results: list[list[str]]):
    """Writes the results of a LaTeX table.

    Attributes:
        f (file): file to be written to.
        results (list[list[str]]): list of lists containing the results of the table.
    """
    for row in results:
        f.write(" & ".join(row))
        f.write(r" \\" + "\n")


def writeTable(headersAndLen: list[tuple[str, int]], subHeaders: list[str], results: list[list[str]], f, caption: str | None = None):
    """Writes a LaTeX table.

    Attributes:
        headersAndLen (list[tuple[str, int]]): list of tuples containing the names of the 
                                               headers and the number of columns they will span.
        subHeaders (list[str]): list of subheaders.
        results (list[list[str]]): list of lists containing the results of the table.
        f (file): file to be written to.
        caption (str | None): caption of the table.
    """
    numCols: int = reduce(lambda x, y: x + y, [
                          headerAndLen[1] for headerAndLen in headersAndLen], 0)

    f.write(r"\begin{table}[h]" + "\n")
    f.write(r"\begin{center}"+"\n")
    f.write(r"\footnotesize"+"\n")
    f.write(r"\begin{tabular}{ |")

    writeTableStart(f, numCols)
    writeHeaders(f, headersAndLen)
    writeSubHeaders(f, headersAndLen, subHeaders)
    f.write(r"\midrule" + "\n")
    writeTableResults(f, results)

    f.write(r"\end{tabular}"+"\n")
    f.write(r"\end{center}"+"\n")
    if caption != None:
        f.write(r"\caption{" + caption + "}\n")
    f.write(r"\end{table}")


def writeStatisticsTables(standards: list[Standard], f) -> None:
    """Writes the statistics tables.

    Attributes:
        standards (list[Standard]): list of standards.
        f (file): file to be written to.
    """
    headersAndLen: list[tuple[str, int]] = [("Standard", 1), ("Parsing", 2),
                                            ("Code Gen", 2), ("Idempotency", 2), ("Correctness", 2), ("All", 2)]

    firstSubHeaders: list[str] = ["PT", "Rel\\%"]

    firstResults = []
    for std in standards:
        row = [std.name]
        for testPhase in testPhasesNames:
            row.append(str(getTestPhaseTNum(std.tests, testPhase)))
            row.append(f"{getTestPhaseRelP(std.tests, testPhase):.2f}")
        row.append(str(getPTNum(std.tests)))
        row.append(f"{getRelP(std.tests):.2f}")
        firstResults.append(row)

    writeTable(headersAndLen, firstSubHeaders, firstResults, f,
               caption="Relative percentage of tests passed")

    secondSubHeaders: list[str] = ["PT", "Abs\\%"]
    secondResults = []
    for std in standards:
        row = [std.name]
        for testPhase in testPhasesNames:
            row.append(str(getTestPhaseTNum(std.tests, testPhase)))
            row.append(f"{getTestPhaseAbsP(std.tests, testPhase):.2f}")
        row.append(str(getPTNum(std.tests)))
        row.append(f"{getAbsP(std.tests):.2f}")
        secondResults.append(row)

    writeTable(headersAndLen, secondSubHeaders, secondResults,
               f, caption="Absolute percentage of tests passed.")
    


def writeStatistics(standards: list[Standard], maxTestPhases: int, f, outputPath) -> None:
    """Writes the Statistics section of the LaTeX report.

    Attributes:
        standards (list[Standard]): a list containing all the standards to be included in the percentage section.
        maxTestsPhases (int): the maximum number of test phases that one test can run. E.g. Parsing, Code Generaiton, Idempotency and Correctness = 4.
        f (file): the file to write the section to.
    """

    f.write(r"\section{Statistics}")
    f.write(r"\subsection{Tables}"+"\n")
    f.write("\\begin{itemize}\n\
            \\item PT: Denotes the number of passed tests / test phases\n\
            \\item RelP: Denotes the percentage of passed tests / test phases. Phases that were not run are disregarded.\n\
            \\item AbsP: Denotes the absolute percentage of passed tests / test phases. Phases that were not run are counted as failures.\n\
            \\end{itemize}\n")

    writeStatisticsTables(standards, f)

    f.write(r"\newpage"+"\n")
    f.write(r"\subsection{Relative Percentage of tests passed chart}"+"\n")
    x_labels = [std.name.capitalize() for std in standards]
    
    success_rel = [getRelP(std.tests) for std in standards]
    failure_rel = [100 - getRelP(std.tests) for std in standards]

    createChart(x_labels, success_rel, failure_rel, "Standards", "Percentage", outputPath)
    
    f.write(r"\subsection{Absolute Percentage of tests passed chart}"+"\n")
    x_labels = [std.name.capitalize() for std in standards]
    
    success_abs = [getAbsP(std.tests) for std in standards]
    failure_abs = [100 - getAbsP(std.tests) for std in standards]

    createChart(x_labels, success_abs, failure_abs, "Standards", "Percentage", outputPath, "", True)


def createChart(xLabels: list[str], sucessRate : list[float], failRate : list[float],
              xMeaning: str, yMeaning: str, outputPath:str ,standard = "", abs = False) -> None:
    """ Draws a chart with the results of the tests for the given standard.

    Attributes:
        xLabels (list[str]): list of labels for the x axis.
        sucessRate (list[float]): list of success rates for each test.
        failRate (list[float]): list of fail rates for each test.
        xMeaning (str): meaning of the x axis.
        yMeaning (str): meaning of the y axis.
        outputPath (str): path to the directory where the chart will be saved.
        standard (str): name of the standard to be included in the title of the chart.
    """
    plt.figure(figsize=(10, 5))
    x_pos = np.arange(len(xLabels))
    width = 0.35
    plt.bar(x_pos - width/2, sucessRate, width, label='Success Rate')
    plt.bar(x_pos + width/2, failRate, width, label='Fail Rate')
    plt.xlabel(xMeaning)
    plt.ylabel(yMeaning)
    if standard != "":
        plt.title('Success and Fail Rate for each test in ' + standard)
    else:
        plt.title('Success and Fail Rate for each standard')
    plt.xticks(x_pos, xLabels)
    plt.legend()
    plt.tight_layout()

    imagesPath = os.path.join(outputPath, "images")
    if not os.path.exists(imagesPath):
        os.makedirs(imagesPath, exist_ok=True)
    
    if standard != "":
        plt.savefig(os.path.join(imagesPath, standard + ".png"))
    else:
        if(abs):
            plt.savefig(os.path.join(imagesPath, "standardsAbs.png"))
        else:
            plt.savefig(os.path.join(imagesPath, "standardsRel.png"))

    plt.close()

    f.write(r"\begin{figure}[h!]"+"\n")
    f.write(r"\centering"+"\n")
    if standard != "":
        f.write(r"\includegraphics[width=0.8\textwidth]{"+imagesPath +"/"+ standard+".png}"+"\n")
        f.write(r"\caption{Success and Fail Rate for each test in " + standard + "}"+"\n")
        f.write(r"\label{fig:"+standard+"}"+"\n")
    else:
        if(abs):
            f.write(r"\includegraphics[width=0.8\textwidth]{"+imagesPath + "/" + "standardsAbs.png}"+"\n")
        else:
            f.write(r"\includegraphics[width=0.8\textwidth]{"+imagesPath + "/" + "standardsRel.png}"+"\n")
        f.write(r"\caption{Success and Fail Rate for each standard}"+"\n")
        f.write(r"\label{fig:standards}"+"\n")
    f.write(r"\end{figure}"+"\n")

def calculatePercentage(testName, results):
    """ Calculates the percentage of success for a given test in a list of results.

    Attributes:
        testName (str): name of the test to be considered.
        results (list[Test]): list of results to be considered.
    
    Returns:
        float: percentage of success for the given test.
    """
    totalCount = len(results)
    successCount = sum(1 for result in results if any(test.name == testName and test.success for test in result.details))
    return successCount / totalCount * 100 if totalCount > 0 else 0

def getPercentagesFromStandard(standard):
    """ Calculates the percentage of success for each test in a given standard.

    Attributes:
        standard (Standard): standard to be considered.

    Returns:
        list[float]: list of percentages of success for each test in the given standard.
    """
    successResults = []
    failedResults = []
    successResults.append(calculatePercentage("test_parsing", standard.tests))
    successResults.append(calculatePercentage("test_code_generation", standard.tests))
    successResults.append(calculatePercentage("test_idempotency", standard.tests))
    successResults.append(calculatePercentage("test_correctness", standard.tests))
    for result in successResults:
        failedResults.append(100-result)
    return successResults, failedResults


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Script to generate a LaTeX report based on CACTI's output")

    parser.add_argument('-S', '--source', dest="src_path", required=True,
                        help='path to the output directory created by CACTI')
    parser.add_argument('-T', '--transpiler', dest="transpiler", required=True,
                        help="name of the desired transpiler. inside the output directory there must be a directory with the transpiler's name")
    parser.add_argument('-O', '--output-path', dest="outputPath", default=os.path.abspath(os.getcwd()),
                        help="path to the directory where the output will be deposited in. A repository named 'reports' will be created.")

    args = parser.parse_args()

    transpiler = args.transpiler
    outputPath = args.outputPath
    outputPath = os.path.join(outputPath, transpiler)

    # creates path to generate the latex file
    # latex_path = os.path.join(root_dir, "report.tex")
    reportPath = os.path.join(outputPath, transpiler)
    if not os.path.exists(reportPath):
        os.makedirs(os.path.dirname(reportPath), exist_ok=True)
    f = open(reportPath + ".tex", "w")

    # different test types folders
    generalPath = os.path.join(args.src_path, transpiler)

    # write usepackages and title to the tex file
    f.write(r"\documentclass{article}"+"\n" +
            r"\usepackage{booktabs}"+"\n"+r"\usepackage{xltabular}"+"\n")
    f.write(r"\usepackage{xcolor}"+"\n")
    f.write(r"\usepackage{graphicx}"+"\n")
    f.write(
        r"\usepackage[top=1.5cm,bottom=3cm,left=1cm,right=1cm,marginparwidth=1.75cm]{geometry}"+"\n"+r"\begin{document}"+"\n")
    f.write(r"\title{" + transpiler.capitalize() + r" Testing Results}"+"\n" +
            r"\maketitle"+"\n"+r"\newcolumntype{Y}{>{\centering\arraybackslash}X}"+"\n")

    standards: list[Standard] = processDirectory(generalPath)[1]
    standards.sort(key=lambda x: getStand(x))

    _, maxTestPhases = findMostCompleteTestInfo(getAllTests(standards))
    writeStandards(standards, f, outputPath)

    writeStatistics(standards, maxTestPhases, f, outputPath)

    f.write(r"\end{document}")
