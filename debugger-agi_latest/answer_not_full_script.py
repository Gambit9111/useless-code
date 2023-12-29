from copy_to_clipboard import load_prompt_from_txt_file, copy_to_clipboard_linux
from luxee_ui_api import send_a_message, get_image_location

file_path = 'prompts/not_full_code_prompt.txt'
share_response_button = "navigation-icons/answer-ready.png"

prompt = load_prompt_from_txt_file(file_path)
copy_to_clipboard_linux(prompt)

send_a_message()

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