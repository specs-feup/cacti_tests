import json
import os
import pylatex


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
    doc.preamble.append(pylatex.Command('begin{tabular}', '{||c c c c c||} '))
    doc.preamble.append(pylatex.NoEscape(r'\hline  & testParsing & testCodeGeneration & testIdempotency & runtime \\ [0.5ex]'))
    
   
    

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
                        # print(json_path)

                            

                        # reads the JSON file
                        with open(json_path) as json_file:
                            parsed_json= json.load(json_file)

                        name = ""
                        tp_success = ""
                        tcg_success = ""
                        ti_success = ""
                        runtime = ""
                
                        for key,value in parsed_json.items():
                            if key == "name":
                                name = parsed_json[key]
                            elif key == "runtime":
                                runtime = parsed_json[key]
                            elif key == "test_parsing":
                                tp_success = parsed_json[key]["success"]
                            elif key == "test_code_generation":
                                tcg_success = parsed_json[key]["success"]
                            elif key == "test_idempotency":
                                ti_success = parsed_json[key]["success"]

                        
                        
                        
                        doc.preamble.append(pylatex.NoEscape(r'\hline {0} & {1} & {2} & {3} & {4} \\'.format(name, tp_success, tcg_success, ti_success, runtime)))

    doc.preamble.append(pylatex.Command('end{tabular}'))
    doc.preamble.append(pylatex.Command('end{document}'))
    doc.generate_tex("report")