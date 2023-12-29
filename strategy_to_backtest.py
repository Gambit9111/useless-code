from gpt_ui_api import start_new_conversation, load_prompt_from_txt_file, send_a_message, scroll_to_the_bottom, download_pdf, upload_file, confirm_script_generated, download_script, send_a_message_v2
import os
import pyautogui
import time

setup_prompt_file_path = "setup-prompts/strategy_to_backtest_prompt.txt"
send_pdf_prompt_file_path = "setup-prompts/send_pdf_prompt.txt"
refine_script_prompt_file_path = "setup-prompts/refine_script_prompt.txt"

directory = 'strategy_pdfs'

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):

        # #? 1) Start new conversation
        start_new_conversation()

        # # # #? 2) send the setup prompt message to gpt
        setup_prompt = load_prompt_from_txt_file(setup_prompt_file_path)
        send_a_message(setup_prompt)

        # # # ? 3) upload the pdf file
        upload_file(filename)

        # # #? 4) send the send pdf prompt message to gpt
        send_pdf_prompt = load_prompt_from_txt_file(send_pdf_prompt_file_path)
        send_a_message(send_pdf_prompt)

        #? 5) confirm that initial script was generated
        initial_script_generated = False
        try_count = 0
        skip_iteration = False

        while not initial_script_generated and try_count <= 10:
            initial_script_generated = confirm_script_generated()
            try_count += 1
            print(f"try count: {try_count}")
            
            if try_count == 10:
                print("Something went wrong, skip this pdf and start from the beginning")
                skip_iteration = True
                break
        
        if skip_iteration:
            # press esc
            pyautogui.press('esc')
            time.sleep(1)
            continue
            
        #? 6)refine the script 2 times
        refine_script_prompt = load_prompt_from_txt_file(refine_script_prompt_file_path)
        for i in range(2):
            send_a_message(refine_script_prompt)

        #? 7) Download the script
        download_script(filename)