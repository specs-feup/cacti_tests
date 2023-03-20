import json
import os


def latexTest(string):
    #remove test_
    reducedString= string[5:]
    latexString=reducedString.replace("_","\_").capitalize()
    return latexString

def latexSource(string):
    latexString=string.replace("_","\_").capitalize()
    return latexString



def latexBool(bool):
    if bool== True:
        latexBool= r"\textcolor{green}{True}"
        return latexBool
    else:
        latexBool= r"\textcolor{red}{False}"
        return latexBool

class Result:
    def __init__(self, name, tests):
        self.name = name
        self.tests= tests
class Test:
    def __init__(self, name, success, time, tries=1):
        self.name = name
        self.success = success
        self.time = time
        if tries !=1 :
            self.tries= tries

if __name__ == '__main__':
    root_dir = './'

    # creates path to generate the latex file
    # latex_path = os.path.join(root_dir, "report.tex")
    f = open("report.tex", "w")

    # different test types folders
    general_path = os.path.join(root_dir, "output")

    # write usepackages and title to the tex file
    f.write(r"\documentclass{article}"+"\n"+r"\usepackage{booktabs}"+"\n"+r"\usepackage{xltabular}"+"\n")
    f.write(r"\usepackage{xcolor}"+"\n")
    f.write(r"\usepackage[top=1.5cm,bottom=3cm,left=1.5cm,right=1cm,marginparwidth=1.75cm]{geometry}"+"\n"+r"\begin{document}"+"\n")
    f.write(r"\title{Clava Testing Results}"+"\n"+r"\maketitle"+"\n"+r"\newcolumntype{Y}{>{\centering\arraybackslash}X}"+"\n")
   
   
    
    results= []
    

    for general_type in os.listdir(general_path):
        general_path = os.path.join(general_path, general_type)
        # loop for different folders
        for type_tests in os.listdir(general_path):
            type_path = os.path.join(general_path, type_tests)
        
            # loops over the various individual folders
            for indiv_tests in os.listdir(type_path):
                indiv_path = os.path.join(type_path, indiv_tests)
            
                # loops over files to find JSON files
                for filename in os.listdir(indiv_path):
                    if filename.endswith('.json'):
                        json_path = os.path.join(indiv_path, filename)    

                        # reads the JSON file
                        with open(json_path) as json_file:
                            parsed_json= json.load(json_file)

                        name = ""
                        time = ""
                        tests= []
                
                        for key,value in parsed_json.items():
                            if key == "name":
                                name = parsed_json[key]
                            else:
                                test = Test(key, parsed_json[key]["success"], parsed_json[key]["time"]) 
                                tests.append(test)

                        result = Result(name, tests)
                        results.append(result)


    # sort tests since they are not granted to be in order
    results.sort(key=lambda x:x.name)
    
    # start table with a column for source file's name and 2 columns per test  
    f.write(r"\begin{xltabular}{\textwidth}{l")
    for x in range(len(results[0].tests)):
        f.write("cc")
    f.write(r"}"+ "\n"+(r"\toprule")+"\n")

    #column with source file's name
    f.write(r"\multicolumn{1}{Y}{}"+"\n")

    for test in results[0].tests:
        f.write(r"& \multicolumn{2}{Y}{\textbf{"+ "{0}".format(latexTest(test.name))+ r"}}")

    f.write(r"\\"+"\n")
    f.write(r"\cmidrule{2-"+str(2*len(results[0].tests)+1)+r"}")

    for test in results[0].tests:
        f.write(r"&Time&Success")
    f.write(r"\\"+"\n")
    f.write(r"\midrule"+"\n")


    # writing result rows
    for result in results:
        row= r"\textbf{" + latexSource(result.name) + r"}"
        for test in result.tests:
           row+= r'& {0}&{1}'.format(test.time, latexBool(test.success))
        row += r' \\[0.5ex]'
        f.write(row+"\n")
    f.write(r"\bottomrule"+"\n")
    f.write(r"\end{xltabular}"+"\n"+r"\end{document}")
  