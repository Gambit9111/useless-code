from gpt_ui_api import start_new_conversation, load_prompt_from_txt_file, send_a_message, scroll_to_the_bottom, download_pdf, send_a_message_v2
import time
import os


#! 1) click the gpt logo X=156, Y=154
#! 2) click the messages tab X=545, Y=947
#! 3) copy paste trascript to strategy prompt
#! 4) wait for gpt to finish the sentance (detect icons)
#! 5) click the messages tab X=545, Y=947
#! 6) copy paste strategy transcript
#! 7) wait for gpt to finish the sentance (detect icons)
#! 8) start 20 pixels right from the icons image, hold the mouse down and slowly scroll up, after each scroll detect the gpt icon, when gpt icon is detected move the mouse to it, then copy the text you just selected

# add a check to make sure we are not going over dublicate links


directory = 'youtube_transcripts'
setup_prompt_file_path = "setup-prompts/transcript_to_strategy_prompt.txt"
transcript_answer_to_pdf_prompt_path = "setup-prompts/get_pdf_prompt.txt"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):

        try:
            transcript_file_path = os.path.join(directory, filename)

            print("Generating trading strategy for: " + transcript_file_path)

            #? 1) Start new conversation
            start_new_conversation()

            #? 2) Load the setup prompt into a variable to pass to gpt
            setup_prompt = load_prompt_from_txt_file(setup_prompt_file_path)

            #? 3) send the setup prompt message to gpt
            send_a_message_v2(setup_prompt)

            # #? 4) send transcript to gpt
            transcript_prompt = load_prompt_from_txt_file(transcript_file_path)
            send_a_message_v2(transcript_prompt)

            # #? 5) get the response in pdf format
            promt = load_prompt_from_txt_file(transcript_answer_to_pdf_prompt_path)
            send_a_message_v2(promt)

            # ? 6) Download the pdf
            download_pdf()
        
            # delete the transcript file
            os.remove(transcript_file_path)
            # time.sleep(900)
        except Exception as e:
            print(e)
            continue
        