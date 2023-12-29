import pyautogui
import time
from PIL import ImageGrab
import time
import subprocess
import shlex

def get_image_location(image):
    location = pyautogui.locateCenterOnScreen(image, confidence=0.9)
    return location

def focus_message_bar():
    try:
        location = get_image_location("navigation-icons/luxee-message-bar.png")
        pyautogui.click(location)
        print(location)
        time.sleep(1)
    except:
        pass

def click_go_to_bottom_button():
    focus_message_bar()
    #move relative to the current position up 100 pixels
    pyautogui.moveRel(0, -100)
    #scroll up just a little bit
    pyautogui.scroll(-1000)

def paste_the_prompt():
    pyautogui.hotkey('ctrl', 'v')
    print("message pasted to message bar")
    time.sleep(1)
    # Send the prompt
    pyautogui.press('enter')


def scroll_up():

    focus_message_bar()
    #move relative to the current position up 100 pixels
    pyautogui.moveRel(0, -100)
    #scroll up just a little bit
    pyautogui.scroll(3)

def download_file():
    
    download_button_file_path = "navigation-icons/download-file-button.png"
    dowloaded_file_name = "strategy.py"
    download_button_visible = False
    
    while download_button_visible == False:
        scroll_up()
        time.sleep(1)
        
        try:
            download_button = get_image_location(download_button_file_path)
        except:
            download_button = None
        
        if download_button != None:
            time.sleep(1)
            download_button_visible = True
            break
    
    download_button = get_image_location(download_button_file_path)
    pyautogui.click(download_button)
    time.sleep(3)
    pyautogui.write(dowloaded_file_name)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    click_go_to_bottom_button()

    
    
        


def send_a_message():
    focus_message_bar()
    paste_the_prompt()
    time.sleep(5)
    click_go_to_bottom_button()    