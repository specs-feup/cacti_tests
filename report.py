import json
import os
from enum import Enum

class standards(Enum):
    stand_11 = 1
    stand_17 = 2
    stand_20 = 3
    stand_98 = 4
    extensions = 5

true_counter = 0
false_counter = 0
unknown_counter = 0


def latexTest(string):
    #remove test_
    reducedString= string[5:]
    latexString=reducedString.replace("_","\_").capitalize()
    return latexString

def latexSource(string):
    latexString=string.replace("_","\_").capitalize()
    return latexString

def latexCamelCase(string):
    words = string.split("\_",1)
    latexString = string
    if (len(words)>1):
        latexString = words[0]+" "+words[1].capitalize()
    return latexString


def latexBool(bool):
    if bool is True:
        latexBool= r"\textcolor{green}{True}"
        global true_counter
        true_counter+=1
        return latexBool
    elif bool is False:
        latexBool= r"\textcolor{red}{False}"
        global false_counter
        false_counter+=1
        return latexBool
    else:
        latexBool= r"N/A"
        global unknown_counter
        unknown_counter+=1
        return latexBool

def getStand(stand):
    if stand.name == "C++98":
        return 1
    elif stand.name == "C++11":
        return 2
    elif stand.name == "C++17":
        return 3
    elif stand.name == "C++20":
        return 4

class Standard:
    def __init__(self, name, result):
        self.name = name
        self.result = result 


class Result:
    def __init__(self, name, tests):
        self.name = name
        self.tests= tests
class Test:
    def __init__(self, name, success, time=0, tries=-1):
        self.name = name
        self.success = success
        self.time = time
        self.tries= tries

if __name__ == '__main__':
    root_dir = './'
    transpiler = os.sys.argv[1]

    # creates path to generate the latex file
    # latex_path = os.path.join(root_dir, "report.tex")
    f = open(transpiler+".tex", "w")

    # different test types folders
    general_path = os.path.join(root_dir, "output/"+transpiler+"/")

    # write usepackages and title to the tex file
    f.write(r"\documentclass{article}"+"\n"+r"\usepackage{booktabs}"+"\n"+r"\usepackage{xltabular}"+"\n")
    f.write(r"\usepackage{xcolor}"+"\n")
    f.write(r"\usepackage[top=1.5cm,bottom=3cm,left=1.5cm,right=1cm,marginparwidth=1.75cm]{geometry}"+"\n"+r"\begin{document}"+"\n")
    f.write(r"\title{" + transpiler.capitalize() + r" Testing Results}"+"\n"+r"\maketitle"+"\n"+r"\newcolumntype{Y}{>{\centering\arraybackslash}X}"+"\n")
   
   
    standards= []
    results= []
    
    for standard_spec in os.listdir(general_path):              # standard folders
        general_path = os.path.join(general_path, standard_spec)   
        for general_type in os.listdir(general_path):           # cpp reference categories
            general_path = os.path.join(general_path, general_type)
            for type_tests in os.listdir(general_path):         # cpp reference subcategories
                type_path = os.path.join(general_path, type_tests)
                for indiv_tests in os.listdir(type_path):       # multiple source files
                    indiv_path = os.path.join(type_path, indiv_tests)
                    for filename in os.listdir(indiv_path):
                        if filename.endswith('.json'):          # loops over files to find JSON files
                            json_path = os.path.join(indiv_path, filename)    
                            with open(json_path) as json_file:  # reads the JSON file
                                parsed_json= json.load(json_file)
                                name = ""
                                time = ""
                                tests= []
                                for key,value in parsed_json.items():
                                    if key == "name":
                                        name = parsed_json[key]
                                    elif key == "test_idempotency":
                                        test = Test(key, parsed_json[key]["success"], tries=len(parsed_json[key]["results"]))
                                        tests.append(test)
                                    else:
                                        if (parsed_json[key]["success"]):
                                            test = Test(key, parsed_json[key]["success"], parsed_json[key]["time"]) 
                                        else:
                                            test = Test(key, False )
                                        tests.append(test)

                                result = Result(name, tests)
                                results.append(result)
        # sort tests since they are not granted to be in order
        results.sort(key=lambda x:x.name)
        stand = Standard(standard_spec, results)
        results=[]
        standards.append(stand)
        general_path = os.path.join(root_dir, "output/"+transpiler+"/")
    
    standards.sort(key=lambda x: getStand(x))

    for standard in standards:
        f.write(r"\section{"+ standard.name + r"}"+"\n")
        # start table with a column for source file's name and 2 columns per test  
        f.write(r"\begin{xltabular}{\textwidth}{l")
        for x in range(len(standard.result[0].tests)):
            f.write("cc")
        f.write(r"}"+ "\n"+(r"\toprule")+"\n")

        #column with source file's name
        f.write(r"\multicolumn{1}{Y}{}"+"\n")

        for test in standard.result[0].tests:
            f.write(r"& \multicolumn{2}{Y}{\textbf{"+ "{0}".format(latexCamelCase(latexTest(test.name)))+ r"}}")

        f.write(r"\\"+"\n")
        f.write(r"\cmidrule{2-"+str(2*len(standard.result[0].tests)+1)+r"}")

        for test in standard.result[0].tests:
            if (test.tries == -1):
                f.write(r"&Time&Success")
            else:
                f.write(r"&Tries&Success")
        f.write(r"\\"+"\n")
        f.write(r"\midrule"+"\n")
        f.write(r"\endhead")

        # writing result rows
        for result in standard.result:
            row= r"\textbf{" + latexSource(result.name) + r"}"
            for test in result.tests:
                if (test.tries == -1):
                    row+= r'& {0}&{1}'.format(test.time, latexBool(test.success))
                else: 
                    row+= r'& {0}&{1}'.format(test.tries, latexBool(test.success))
            row += r' \\[0.5ex]'
            f.write(row+"\n")
        f.write(r"\bottomrule"+"\n")
        f.write(r"\end{xltabular}"+"\n")
        f.write(r"\newpage" + "\n")
    f.write(r"\section{Percentages}")
    f.write("Percentage of passed tests:\n")
    f.write(str(round(true_counter/(false_counter+unknown_counter+true_counter)*100,2))+r" \%")
    f.write(r"\end{document}")
  