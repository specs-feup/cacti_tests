import json
import os

root_dir = './'

# generate the latex file
latex_path = os.path.join(root_dir, "report.tex")

for general_type in os.listdir(root_dir):

    # different test types folders
    general_path = os.path.join(root_dir, general_type)

    # filters out files
    if not os.path.isdir(general_path) or general_path == './.git':
        continue
    
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
                    # with open(json_path, 'r') as f:
                    # TODO

                
        