import json
import os



class Result:
    def __init__(self, name, runtime, tests):
        self.name = name
        self.runtime = runtime
        self.tests= tests
class Test:
    def __init__(self, name, success):
        self.name = name
        self.success = success

if __name__ == '__main__':
    root_dir = './'

    # creates path to generate the latex file
    # latex_path = os.path.join(root_dir, "report.tex")
    f = open("report.tex", "w")

    # different test types folders
    general_path = os.path.join(root_dir, "output")



  #  with doc.create(pylatex.Section("Clava results")):
        
    f.write(r"\documentclass{article}"+"\n"+r"\usepackage{booktabs}"+"\n"+r"\usepackage{longtable}"+"\n")
    f.write(r"\usepackage[top=1.5cm,bottom=3cm,left=1.5cm,right=1cm,marginparwidth=1.75cm]{geometry}"+"\n"+r"\begin{document}"+"\n")
    f.write(r"\title{Clava Testing Results}"+"\n"+r"\maketitle"+"\n")
   
   # doc.preamble.append(pylatex.Command('begin{tabular}', '{||c c c c c} '))
    
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
                        runtime = ""
                        tests= []
                
                        for key,value in parsed_json.items():
                            if key == "name":
                                name = parsed_json[key]
                            elif key == "runtime":
                                runtime = parsed_json[key]
                            else:
                                test = Test(key, parsed_json[key]["success"]) 
                                tests.append(test)

                        result = Result(name, runtime, tests)
                        results.append(result)
    
    results.sort(key=lambda x:x.name)
    f.write(r"\begin{longtable}{lr")
    for x in range(len(results[0].tests)):
        f.write("c")
    f.write(r"}"+ "\n"+ r"\toprule"+"\n")

    
    
    
    
    
    header = r'& Runtime' 
    for test in results[0].tests:
        header+= r'& {0}'.format(test.name.replace("_","\_").capitalize())

    header+= r'\\[0.5ex]'
    f.write(header+"\n"+r"\midrule"+"\n")


    for result in results:
        row= r'{0} & {1}'.format(result.name.replace("_","\_"), result.runtime)
        for test in result.tests:
            row+= r'& {0}'.format(test.success)
        row += r' \\[0.5ex]'
        f.write(row+"\n")
    f.write(r"\bottomrule"+"\n")
    f.write(r"\end{longtable}"+"\n"+r"\end{document}")
  