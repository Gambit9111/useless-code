import sys
import traceback


# Redirect stderr to a file
sys.stderr = open('strategy_error_log.txt', 'w')

script_file = "strategy.py"
result_file = "executed.txt"

strategy_error = True

try:
    # Execute the Python script
    exec(open(script_file).read())
    print("Executed " + script_file)
    strategy_error = False
except Exception as e:
    # Print the error to stderr
    # Print the error traceback to stderr
    strategy_error = True
    traceback.print_exc(file=sys.stderr)
finally:
    print(strategy_error)
    # Write the result to a file
    with open(result_file, 'w') as file:
        file.write(str(strategy_error))  # Write True if no error, False if error
    sys.stderr.close()