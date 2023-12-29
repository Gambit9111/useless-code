from gpt_ui_api import start_new_conversation, load_prompt_from_txt_file, send_a_message, scroll_to_the_bottom, download_pdf, send_a_message_v2, upload_file, confirm_script_generated
import time
import os
import pyautogui

#! 1) click the gpt logo X=156, Y=154
#! 2) click the messages tab X=545, Y=947
#! 3) copy paste trascript to strategy prompt
#! 4) wait for gpt to finish the sentance (detect icons)
#! 5) click the messages tab X=545, Y=947
#! 6) copy paste strategy transcript
#! 7) wait for gpt to finish the sentance (detect icons)
#! 8) start 20 pixels right from the icons image, hold the mouse down and slowly scroll up, after each scroll detect the gpt icon, when gpt icon is detected move the mouse to it, then copy the text you just selected

# add a check to make sure we are not going over dublicate links


directory = 'paper_input'
setup_prompt_file_path = "setup-prompts/papers_to_strategy.txt"
transcript_answer_to_pdf_prompt_path = "setup-prompts/get_pdf_prompt.txt"

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):

        try:
            print("Generating trading strategy for: " + filename)

            #? 1) Start new conversation
            start_new_conversation()

            #? 2) Load the setup prompt into a variable to pass to gpt
            setup_prompt = load_prompt_from_txt_file(setup_prompt_file_path)

            #? 3) send the setup prompt message to gpt
            send_a_message_v2(setup_prompt)

            # # # ? 3) upload the pdf file
            upload_file(filename)
            time.sleep(5)
            #? 5) get the response in pdf format
            promt = load_prompt_from_txt_file(transcript_answer_to_pdf_prompt_path)
            send_a_message(promt)

            #? 5) get the response in pdf format
            promt = load_prompt_from_txt_file(transcript_answer_to_pdf_prompt_path)
            send_a_message(promt)
        
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

            # ? 6) Download the pdf
            download_pdf()
        
            # delete the transcript file
            filepath = os.path.join(directory, filename)
            os.remove(filepath)
            # time.sleep(900)
        except Exception as e:
            print(e)
            continue
        