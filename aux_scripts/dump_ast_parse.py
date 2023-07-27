#! /bin/python3

# Requires clang-tools in ubuntu

import subprocess
import re
import argparse
import subprocess
import re


def filter_ast_dump_output(file_path: str) -> None:
    """Filters and displays the AST dump output of a given C/C++ file

    Attributes:
        file_path (str): Path to the input C/C++ file
    """

    try:
        # Execute clang-check command and capture the output
        command: list[str] = ["clang-check", "-ast-dump", file_path]
        output: str = subprocess.check_output(
            command, universal_newlines=True, stderr=subprocess.PIPE)

        # Filter and display the matching lines
        pattern = re.compile(r'<.*Data>')
        for line in output.splitlines():
            if pattern.search(line):
                print(line)
    except subprocess.CalledProcessError as e:
        print(
            f"Command execution failed with error code {e.returncode}: {e.stderr}")
    except FileNotFoundError:
        print("clang-check command not found. Please ensure Clang is installed and added to the system's PATH.")


parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description="Script to dump Clang's generated AST of a given C/C++ file")
parser.add_argument('-S', '--source', dest="file_path",
                    required=True, help="Path to the input C/C++ file")
args: argparse.Namespace = parser.parse_args()
filter_ast_dump_output(args.file_path)
