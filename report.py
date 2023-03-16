import json
import os


if __name__ == '__main__':
    root_dir = './'

    # creates path to generate the latex file
    latex_path = os.path.join(root_dir, "report.tex")

    # different test types folders
    general_path = os.path.join(root_dir, "output")

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
                    print(parsed_json)
                    # TODO