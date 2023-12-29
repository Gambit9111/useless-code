import pyautogui
import time
from PIL import ImageGrab
import time
import subprocess
import shlex


# Function to copy text to the clipboard using xclip
def copy_to_clipboard_linux(text):
    subprocess.run(['xclip', '-selection', 'c'], input=text, text=True)

def get_image_location(image):
    location = pyautogui.locateCenterOnScreen(image, confidence=0.8)
    return location

def start_new_conversation():
    
    print("Starting new conversation with GPT")
    try:
        location = get_image_location("gpt-icons/gpt-logo-start.png")
        pyautogui.click(location)
        time.sleep(5)
    except:
        pass

def load_prompt_from_txt_file(filepath):
    
    print("Loading prompt from file: " + filepath)
    try:
        with open(filepath, 'r') as file:
            prompt = file.read()
        print(prompt)
        return prompt
    except:
        pass

def check_screenshot_change(x1, y1, x2, y2):
    while True:
        # Take the first screenshot
        screenshot1 = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
        time.sleep(10)
    
        # Take the second screenshot
        screenshot2 = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
        # Check if the screenshots are different
        if screenshot1.tobytes() != screenshot2.tobytes():
            print("Work in progress, please wait...")
            continue
        else:
            print("Work is done, continue")
            break

def send_a_message(message):
    
    print("Sending message to GPT")
    x1, y1, x2, y2 = 400, 820, 800, 920  # text area coordinates
    #? 1) Focus the message bar to type the prompt
    try:
        location = get_image_location("gpt-icons/gpt-message-bar.png")
        pyautogui.click(location)
        time.sleep(3)
    except:
        pass
    
    #? 2) Type the prompt
    pyautogui.write(message)
    check_screenshot_change(x1, y1, x2, y2)
    # #? 3) Send the prompt
    pyautogui.press('enter')
    time.sleep(5)
    
    gpt_answering = True
    
    while gpt_answering:
        print("Please wait GPT is generating an answer")
        try:
            location = get_image_location("gpt-icons/gpt-answering.png")
            time.sleep(5)
        except:
            gpt_answering = False
            print("GPT Has generated an answer, continue")

def send_a_message_v2(message):
    
    try:
        location = get_image_location("gpt-icons/gpt-message-bar.png")
        pyautogui.click(location)
        time.sleep(3)
    except:
        pass
    
    #? 2) Type the prompt
    # Copy the contents of the script to the clipboard
    copy_to_clipboard_linux(message)
    print("message copied to clipboard")
    # Paste the contents of the clipboard into the message bar
    pyautogui.hotkey('ctrl', 'v')
    print("message pasted to message bar")
    time.sleep(3)
    # Send the prompt
    pyautogui.press('enter')
    
    time.sleep(5)
    gpt_answering = True
    
    while gpt_answering:
        print("Please wait GPT is generating an answer")
        try:
            location = get_image_location("gpt-icons/gpt-answering.png")
            time.sleep(5)
        except:
            gpt_answering = False
            print("GPT Has generated an answer, continue")

def scroll_to_the_bottom():
    print("Scrolling to the bottom of the page")
    pyautogui.moveTo(400,400)
    pyautogui.scroll(-1000)

def download_pdf():
    
    print("Downloading the pdf")
    scroll_to_the_bottom()
    time.sleep(5)
    try:
        location = pyautogui.locateCenterOnScreen("gpt-icons/download-button.png", confidence=0.9)
        pyautogui.click(location)
        time.sleep(5)
        print("Download button found")
    except:
        pass
    
    try:
        location = get_image_location("gpt-icons/save-pdf-button.png")
        pyautogui.click(location)
        time.sleep(3)
        print("Save pdf button found")
    except:
        pass
    
    print("Saving the pdf")
    # press enter to save the pdf
    pyautogui.press('enter')
    time.sleep(3)
    
    print("Closing the pdf")
    # press ctrl+w to close the pdf
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(3)

def upload_file(filename):
    print("Uploading file: " + filename)
    try:
        location = get_image_location("gpt-icons/upload-file-button.png")
        pyautogui.click(location)
        time.sleep(5)
    except:
        pass

    try:
        location = get_image_location("gpt-icons/search-file-button.png")
        pyautogui.click(location)
        time.sleep(5)
    except:
        pass
    
    pyautogui.write(filename)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
    print("File uploaded")


def confirm_script_generated():
    print("Confirming the script is generated")
    time.sleep(10)
    scroll_to_the_bottom()
    time.sleep(5)
    try:
        location = pyautogui.locateCenterOnScreen("gpt-icons/download-button.png", confidence=0.9)
        time.sleep(3)
        print("Download button found, script generated")
        return True
    except:
        print("Download button not found, give it more time")
        return False
    
def download_script(filename):
    
    print("Downloading the script")
    scroll_to_the_bottom()
    time.sleep(5)
    try:
        location = pyautogui.locateCenterOnScreen("gpt-icons/download-button.png", confidence=0.9)
        pyautogui.click(location)
        time.sleep(5)
        print("Download button found")
    except:
        pass
    
    print("Saving the script")
    # press enter to save the pdf
    pyautogui.press('enter')
    time.sleep(3)
    #remove .pdf from filename
    filename = filename[:-4]
    # add .py to filename
    pyautogui.write(filename)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    print("Script saved")

# x, y = get_image_location("gpt-finished-talking-icons.png")

# print(x, y)

# x = x + 115
# y = y - 30

# pyautogui.click(x, y)