import networkx as nx  ## dependency
import os
from os import path
import argparse
import json
from matplotlib import pyplot as plt  ## dependency
from pyvis.network import Network ## dependency
from colorama import Fore, Style ## dependency

# Note: The output graph may not be readable for very dense or very large graphs

JSON_NODE_LIST_KEY = "extraNodes"


def handleParsing() -> argparse.Namespace:
    """Adds the arguments necessary to run the program to the argparser, checks for arguments that need others in order to function properly and returns the Namespace object with the arguments."""
    parser = argparse.ArgumentParser(
        description="Script that generates a dependency graph between the tests.")

    parser.add_argument('-s', '--source', dest="srcPath", required=True,
                        help="path to the directory with the test files.")
    parser.add_argument('-c', '--cycles', action='store_true', dest="listCycles",
                        default=False, help="print all the cycles found to standard output.")
    parser.add_argument('-l', '--leaves', action='store_true', dest="listLeaves", default=False,
                        help="print all the leaf nodes, that is, nodes with no dependencies.")
    parser.add_argument('-v', '--visual', action='store_true', dest="showGraph", default=False,
                        help="open a pop-up window that allows for a visual analysis of the graph.")
    parser.add_argument('-S', '--save', dest="outputPath",
                        help="save an svg of the visual representation of the graph to a given directory.")
    parser.add_argument('-f', '--format', dest="format", default="SVG",
                        help="Specify a file format to save the visual representation in. Must be supported by pyplot's savefig.")

    ret = parser.parse_args()

    if "format" in vars(ret) and "outputPath" not in vars(ret):
        print(Fore.RED + Style.BRIGHT +
              "--format requires --save. Nothing will be saved." + Style.RESET_ALL)

    return ret


def constructGraph(sourcePath: str) -> nx.DiGraph:
    """Constructs a dependency graph of the tests in the specified directory. The tests must abide by cacti's test directory specification.

    Attributes:
        sourcePath (str): path to the tests directory.

    Returns:
        nx.DiGraph: networkx's Directed Graph representation of the dependencies between tests.
    """
    dependencyGraph: nx.DiGraph = nx.DiGraph()

    for root, _, files in os.walk(path.abspath(sourcePath)):
        for isDependentOf in files:
            filePath: str = path.join(root, isDependentOf)
            if not isEligibile(filePath):
                continue
            try:
                testName: str = path.basename(path.dirname(filePath))
                f = open(filePath)
                extraNodes: list[str] = json.loads(
                    f.read())[JSON_NODE_LIST_KEY]

                for isDependentOf in extraNodes:  # the test that is named testName is dependent on isDependentOf
                    if isDependentOf == testName:
                        print(isDependentOf + " is a self cycle")
                    dependencyGraph.add_edge(testName, isDependentOf)

            except Exception as e:
                print("Error while trying to read json data from " +
                      filePath + ":" + str(e))

            finally:
                f.close()

    return dependencyGraph


def isEligibile(filePath: str) -> bool:
    """Checks if a file is a valid to be parsed into relevant information for the dependency graph."""
    if not path.basename(filePath) == "metadata.json":
        return False
    try:
        f = open(filePath)
        content = f.read()
        jsonContent = json.loads(content)
        return JSON_NODE_LIST_KEY in jsonContent

    except Exception as e:
        print("Error while trying to parse " + filePath + ": " + str(e))
        return False

    finally:
        f.close()


def printCycles(graph: nx.DiGraph) -> None:
    """Finds cycles in the given graph and prints it to standard output."""
    cycles: list[list[str]] = list(nx.simple_cycles(graph))
    if (len(cycles) == 0):
        print(Fore.YELLOW + Style.BRIGHT + "There are no cycles in the graph." + Style.RESET_ALL)
        return
    cycles.sort(key= lambda x: x[0])

    print(f"There are {len(cycles)} cycles:")
    for cycle in cycles:
        print("- ", end="")
        for index, node in enumerate(cycle):
            print(node, end="")
            if index == len(cycle) - 1:
                continue
            print(" -> ", end="")
        print("")

    print("")


def findLeaves(graph: nx.DiGraph) -> list[str]:
    """Finds the leaf nodes of the given graph and returns them as a list."""
    leafNodes: list[str] = list()
    for node in graph.nodes:
        if len(list(graph.adj[node])) == 0:
            leafNodes.append(node)
    return leafNodes


def printLeaves(graph: nx.DiGraph) -> None:
    """Finds the leaf nodes of the graph and prints them to standard output."""
    leafNodes = findLeaves(graph)

    if (len(leafNodes) == 0):
        print(Fore.YELLOW + Style.BRIGHT + "There are no leaf nodes." + Style.RESET_ALL)

    print(f"There are {len(leafNodes)} ({(len(leafNodes) / len(graph.nodes) * 100):.2f}%) leaves:")
    for node in leafNodes:
        print(node)
    print("")


def showGraph(graph: nx.DiGraph) -> None:
    """Opens a pyplot pop-up window showing a visual representation of the graph."""
    net = Network(notebook=True)
    net.from_nx(graph)
    net.toggle_physics(False)
    net.show("example.html")


def saveGraph(graph: nx.DiGraph, outputPath: str, format: str) -> None:
    """Saves a visual representation of the graph in a given directory and in a given format, as long as pyplot.savefig supports it."""
    plt.tight_layout()
    nx.draw_networkx(dependencyGraph, arrows=True)
    savePath = path.abspath(path.join(outputPath, "dependencyGraph." + format.lower()))
    plt.savefig(savePath, format=format)
    print(Fore.GREEN + Style.BRIGHT + "File saved to " + savePath + Style.RESET_ALL)


if __name__ == "__main__":

    args: argparse.Namespace = handleParsing()

    sourcePath: str = args.srcPath
    dependencyGraph: nx.DiGraph = constructGraph(sourcePath)

    if args.listCycles:
        printCycles(dependencyGraph)
    if args.listLeaves:
        printLeaves(dependencyGraph)
    if args.outputPath:
        saveGraph(dependencyGraph, args.outputPath, args.format)
    if args.showGraph:
        showGraph(dependencyGraph)
    plt.clf()
