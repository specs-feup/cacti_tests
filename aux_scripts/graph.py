import networkx as nx ## dependency
import os
from os import path
import argparse
import json
from matplotlib import pyplot as plt ## dependency

# Note: The output graph may not be readable for very dense or very large graphs

JSON_NODE_LIST_KEY = "extraNodes"

def isEligibile(filePath: str) -> bool:
    if not path.basename(filePath) == "metadata.json": return False
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
        

if __name__  == "__main__":
    dependencyGraph: nx.DiGraph = nx.DiGraph()

    parser = argparse.ArgumentParser(description="Script that generates a dependency graph between the tests.")
    parser.add_argument('-S', '--source', dest="srcPath", required=True, help="path to the directory with the files.")
    parser.add_argument('-O', '--output-path', dest="outputPath", default=".", help="path to the directory to save the picture of the generated dependency graph in")

    args = parser.parse_args()

    sourcePath: str = args.srcPath
    
    for root, _, files in os.walk(path.abspath(sourcePath)):
        for isDependentOf in files:
            filePath: str = path.join(root, isDependentOf)
            if not isEligibile(filePath): continue
            try:
                testName: str = path.basename(path.dirname(filePath))
                f = open(filePath)
                extraNodes: list[str] = json.loads(f.read())[JSON_NODE_LIST_KEY]

                for isDependentOf in extraNodes: # the test that is named testName is dependent on isDependentOf
                    if isDependentOf == testName:
                        print(isDependentOf + " is a self cycle")
                    dependencyGraph.add_edge(testName, isDependentOf)
                
            except Exception as e:
                print("Error while trying to read json data from " + filePath + ":" + str(e))
            
            finally:
                f.close()

    output: str = args.outputPath
    plt.tight_layout()
    nx.draw_networkx(dependencyGraph, arrows=True)
    plt.savefig(path.join(output, "dependencyGraph.svg"), format="SVG")
    plt.show()
    plt.clf()
    
    

