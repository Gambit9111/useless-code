import difflib
import re

def compare_python_script_with_file(script_file_name):
    with open(script_file_name, 'r') as file:
        python_script_lines = file.readlines()

    with open('not_full_code.txt', 'r') as file:
        not_full_code_lines = file.readlines()

    for python_line in python_script_lines:
        for code_line in not_full_code_lines:
            if difflib.SequenceMatcher(None, python_line, code_line).ratio() > 0.8:
                return True  # Return True as soon as a match is found

    return False  # If no match is found

def count_lines_in_python_script(script_file_name):
    with open(script_file_name, 'r') as file:
        lines = file.readlines()
        return len(lines)

# Example usage
result = compare_python_script_with_file('strategy.py')
print("Match found:", result)

num_lines = count_lines_in_python_script('strategy.py')
print("Number of lines in the script:", num_lines)