from copy_to_clipboard import load_prompt_from_txt_file, copy_to_clipboard_linux
from luxee_ui_api import send_a_message

file_path = 'prompts/setup_prompt.txt'

prompt = load_prompt_from_txt_file(file_path)
copy_to_clipboard_linux(prompt)

send_a_message()