# CACTI Tests

This repository holds the C/C++ source files that represent various features of each language.

## About CACTI 

**CACTI** (**C**ompiler **A**nalysis, **C**omparison & **T**esting **I**nfrastructure) is a project being developed by four software-engineering students, for the Capstone Project curricular unit.

As the name suggests, CACTI wishes to study and compare the capabilities of different compilers, by collecting/creating several input C and C++ files that represent various functionalities of each language, and by defining and implementing tests for each transpiliation task (parsing, code generation, querying and transformation).

## Members

### Students 
- Fábio Morais (<a href="https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=202008052">202008052</a>) - Faculty of Engineering, University of Porto, Portugal
- Francisco Prada (<a href="https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=202004646">202004646</a>) - Faculty of Engineering, University of Porto, Portugal
- Guilherme Sequeira (<a href="https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=202004648">202004648</a>) - Faculty of Engineering, University of Porto, Portugal
- Pedro Ramalho (<a href="https://sigarra.up.pt/feup/pt/fest_geral.cursos_list?pv_num_unico=202004715">202004715</a>) - Faculty of Engineering, University of Porto, Portugal

### Tutors

- <a href="https://sigarra.up.pt/feup/pt/func_geral.formview?p_codigo=519965">João Bispo</a> - Faculty of Engineering, University of Porto, Portugal
- <a href="https://sigarra.up.pt/feup/pt/func_geral.formview?p_codigo=662695">Luís Sousa</a> - Faculty of Engineering, University of Porto, Portugal

## Important scripts

Most of the scripts of this directory are inside the **aux_scripts** folder. Here is a compilation on how to run some of them:

### Generate Report
```
$ python3 report.py [-h] -S SRC_PATH -T TRANSPILER
```

- `-S SRC_PATH` - specify the path to the directory where the generated outputs are
- `-T TRANSPILER` - the name of the transpiler which is to be tested

### Generate the metadata

```
$ python3 metadata_gen.py [-h] -S SRC_PATH
```
- `-S SRC_PATH` -  specify the path to the directory where the tests currently are

### Extract keywords

```
$ python3 extract_keywords.py <directory_path>
```
- `<directory_path>` - define the directory to extract the keywords from

### Extract the keywords from a single file

```
python3 extract_single_file_keywords.py <cpp_standard> <file_path>
```
- `<cpp_standard>` -  specify from which standard are the desired keywords
- `<file_path>` - identify the path of the file from which the keywords should be extracted

### Create graph with the generated nodes

```
$ python3 graph.py [-h] -S SRC_PATH [-c] [-l] [-v] [-O OUTPUT_PATH] [-F FORMAT]
```
- `-S SRC_PATH` - path to the directory with the test files.
- `-c` - print all the cycles found to standard output.
- `-l` - print all the leaf nodes, that is, nodes with no dependencies.
- `-v` - open a pop-up window that allows for a visual analysis of the graph.
- `-O OUTPUT_PATH` - save an svg of the visual representation of the graph to a given directory.
- `-F FORMAT` - Specify a file format to save the visual representation in. Must be supported by pyplot's savefig. 

## Sources

- [cppreference](https://en.cppreference.com) - 
the source files in this repository were adapted from the example code available here.