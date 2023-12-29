import subprocess
import time
from full_code_answer_check import compare_python_script_with_file, count_lines_in_python_script

setup_prompt_script = 'build_setup_prompt.py'
setup_prompt_ran = False

run_strategy_script = 'run_strategy.py'
answer_prompt_script = 'build_answer_prompt.py'
download_file_script = 'download_file.py'
answer_not_full_script = 'answer_not_full_script.py'

number_of_lines_in_the_previous_script = 0
number_of_lines_in_the_new_script = 0

def run_script(script):
    try:
        # Run the python script using subprocess
        subprocess.run(['python', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

while True:
    if not setup_prompt_ran:
        run_script(setup_prompt_script)
        time.sleep(5)
        setup_prompt_ran = True
        print("Setup prompt ran")
    
    result = compare_python_script_with_file('strategy.py')
    number_of_lines_in_the_previous_script = count_lines_in_python_script('strategy.py')
    if result == True:
        run_script(answer_not_full_script)
        time.sleep(3)
        run_script(download_file_script)
        time.sleep(3)
        continue

    run_script(run_strategy_script)
    time.sleep(3)

    with open("executed.txt", "r") as file:
        result = file.read().strip()
        if result == "False":
            print("Script execute successfully. Terminating...")
            sys.exit(1)
        else:
            print("Script did not execute, continue debugging")

    run_script(answer_prompt_script)
    time.sleep(3)
    run_script(download_file_script)
    time.sleep(3)
    number_of_lines_in_the_new_script = count_lines_in_python_script('strategy.py')

    # Calculate 80% of the lines in the previous script
    threshold = 0.8 * number_of_lines_in_the_previous_script
    
    print("waiting for another script to run...")

    # Check if the number of lines in the new script is not less than 80% of the previous script number
    if number_of_lines_in_the_new_script >= threshold:
        print("Number of lines in the new script is not less than 80% of the previous script number.")
    else:
        run_script(answer_not_full_script)
        time.sleep(5)
        run_script(download_file_script)
        time.sleep(5)
        continue