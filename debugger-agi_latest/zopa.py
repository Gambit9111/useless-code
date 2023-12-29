import subprocess

def run_script(script):
    try:
        # Run the python script using subprocess
        result = subprocess.run(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            # Script executed successfully
            print(f"Script {script} executed successfully.")
            return True
        else:
            # Script did not execute successfully
            print(f"Error running {script}. Process return code: {result.returncode}")
            return False
    
    except Exception as e:
        print(f"Error running {script}: {e}")
        return False

# Usage example
script_path = "run_strategy.py"
execution_result = run_script(script_path)
print("Script executed:", execution_result)