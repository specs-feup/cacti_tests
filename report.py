import json
import os
import pylatex




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
    latex_path = os.path.join(root_dir, "report.tex")

    # different test types folders
    general_path = os.path.join(root_dir, "output")



  #  with doc.create(pylatex.Section("Clava results")):
        

    doc = pylatex.Document()
    doc.preamble.append(pylatex.Command('title', 'Clava tests'))
    doc.preamble.append(pylatex.Command('begin{document}'))
    doc.preamble.append(pylatex.Command('maketitle'))
    doc.preamble.append(pylatex.Command('begin{tabular}', '{||c c c c c} '))
    
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

    header = r'\hline && runtime' 
    for test in results[0].tests:
        header+= r'&& {0}'.format(test.name.replace("_","\_"))

    header+= r'\\'
    doc.preamble.append(pylatex.NoEscape(header))


    for result in results:
        row= r'\hline {0} && {1}'.format(result.name.replace("_","\_"), result.runtime)
        for test in result.tests:
            row+= r'&& {0}'.format(test.success)
        row += r' \\'
        doc.preamble.append(pylatex.NoEscape(row))
    
    
    doc.preamble.append(pylatex.Command('end{tabular}'))
    doc.preamble.append(pylatex.Command('end{document}'))
    doc.generate_tex("report")
