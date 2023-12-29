#Delete the answer_prompt.txt file
import os
from copy_to_clipboard import load_prompt_from_txt_file, copy_to_clipboard_linux
from luxee_ui_api import send_a_message, get_image_location
import time

file_path = 'prompts/answer_prompt.txt'
prompt_builder1 = 'prompts/prompt_builder1.txt'
prompt_strategy = 'strategy.py'
prompt_builder2 = 'prompts/prompt_builder2.txt'
prompt_error_log = 'strategy_error_log.txt'
prompt_builder3 = 'prompts/prompt_builder3.txt'

share_response_button = "navigation-icons/answer-ready.png"

if os.path.exists(file_path):
    os.remove(file_path)

# Open strategy.py and read its content
with open(prompt_builder1, 'r') as input_file:
    content = input_file.read()

# Append the content to answer_prompt.txt
with open(file_path, 'a') as output_file:
    output_file.write(content)

# Open strategy.py and read its content
with open(prompt_strategy, 'r') as input_file:
    content = input_file.read()

# Append the content to answer_prompt.txt
with open(file_path, 'a') as output_file:
    output_file.write(content)

# Open strategy.py and read its content
with open(prompt_builder2, 'r') as input_file:
    content = input_file.read()

# Append the content to answer_prompt.txt
with open(file_path, 'a') as output_file:
    output_file.write(content)
    
# Open strategy.py and read its content
with open(prompt_error_log, 'r') as input_file:
    content = input_file.read()

# Append the content to answer_prompt.txt
with open(file_path, 'a') as output_file:
    output_file.write(content)

# Open strategy.py and read its content
with open(prompt_builder3, 'r') as input_file:
    content = input_file.read()

# Append the content to answer_prompt.txt
with open(file_path, 'a') as output_file:
    output_file.write(content)

prompt = load_prompt_from_txt_file(file_path)
copy_to_clipboard_linux(prompt)

send_a_message()
time.sleep(5)

#make sure the script will exit only after share_response_button is visible
share_response_button_visible = False

while share_response_button_visible == False:
    try:
        share_response_button_location = get_image_location(share_response_button)
    except:
        share_response_button_location = None
    
    if share_response_button_location != None:
        share_response_button_visible = True
        break

print("Response Generated")