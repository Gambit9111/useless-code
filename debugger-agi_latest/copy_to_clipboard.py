import subprocess
import shlex

def load_prompt_from_txt_file(filepath):
    
    print("Loading prompt from file: " + filepath)
    try:
        with open(filepath, 'r') as file:
            prompt = file.read()
        print(prompt)
        return prompt
    except:
        pass

# Function to copy text to the clipboard using xclip
def copy_to_clipboard_linux(text):
    subprocess.run(['xclip', '-selection', 'c'], input=text, text=True)
