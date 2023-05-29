# To install dependencies run '-pip install -r dependencies.txt' on terminal
import cv2
import numpy as np
import pyautogui
import time
import requests
import os
import json
import threading
import random
import pygame
from PIL import Image
from screeninfo import get_monitors
from pathlib import Path


# Gets user data
def load_data_from_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    script_dir = os.path.join(parent_dir, "script")

    json_path = os.path.join(script_dir, "userData.json")

    default_data = {
        "TOKEN": "",
        "CHANNEL_URL": "",
        "DM_URL": "",
        "BOT_TOKEN": ""
    }

    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
            # Add any missing keys to the loaded data
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
    else:
        data = default_data
    
    return data

# Path 
p1 = Path(__file__)
p1 = p1.parent.parent.absolute()
path = str(p1)
print(path)

# Load data from userData.json
data = load_data_from_json()
TOKEN = data["TOKEN"]
CHANNEL_URL = data["CHANNEL_URL"]
DM_URL = data["DM_URL"]
BOT_TOKEN = data["BOT_TOKEN"]

# Global thread var
stop_event = threading.Event()

class pokebot():
    @staticmethod
    def spawn_pokemon():
        while not stop_event.is_set():

            # Check again here if the thread should stop
            if stop_event.is_set():
                break
            
            # Sends ;p commands every random interval
            header = {
                'authorization': TOKEN,
            }
            payload = {
                'content': ";p"
            }

            # Check again here if the thread should stop
            if stop_event.is_set():
                break

            r = requests.post(CHANNEL_URL, data=payload, headers=header)

            # Check again here if the thread should stop
            if stop_event.is_set():
                break
                    
            # checks for keyword to stop script
            VERIFICATION_KEYWORD = "You must wait until"
            r = requests.get(CHANNEL_URL, headers=header)
            messages = r.json()
            for message in messages:
                if VERIFICATION_KEYWORD.lower() in message['content'].lower():
                # send a DM using alt account
                    header = {
                        'authorization': BOT_TOKEN,
                    }
                    payload = {
                        'content': "Script stopped because wait message"
                    }
                    stop_event.set()
                    return
            randomSleep = (random.randint(1000,1500))/100.0
            print(f"Sleeping for {randomSleep}")
            time.sleep(randomSleep)
            # Check again here if the thread should stop
            if stop_event.is_set():
                break

    @staticmethod
    def throw_pokeball():
        while not stop_event.is_set():
            # Specify the index of the screen you want to capture (e.g., 0 for the first screen)
            screen_index = 0
            
            # Images path
            detectLeg = cv2.imread(path + '\\detectLeg.png')
            detectRare = cv2.imread(path + '\\detectRare.png')
            pokeball = cv2.imread(path + '\\pokeball.png')
            superball = cv2.imread(path + '\\superball.png')
            ultraball = cv2.imread(path + '\\ultraball.png')
        
            # Check again here if the thread should stop
            if stop_event.is_set():
                break

            # Get the resolution of the specified screen
            screen = get_monitors()[screen_index]
            screen_width, screen_height = screen.width, screen.height

            # Capture a screenshot of the specified screen
            screenshot = pyautogui.screenshot(region=(screen.x, screen.y, screen_width, screen_height))
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

            # Perform template matching to find the detectLeg and detectRare images in the screenshot
            result_leg = cv2.matchTemplate(screenshot, detectLeg, cv2.TM_CCOEFF_NORMED)
            _, max_val_leg, _, _ = cv2.minMaxLoc(result_leg)

            result_rare = cv2.matchTemplate(screenshot, detectRare, cv2.TM_CCOEFF_NORMED)
            _, max_val_rare, _, _ = cv2.minMaxLoc(result_rare)
            
            # Specify a threshold for template matching confidence
            threshold = 0.9
            
            # If detectLeg is detected, find and click ultraball. If detectRare is detected, find and click superball. Else, find and click pokeball.
            if max_val_leg >= threshold:
                ball = ultraball
            elif max_val_rare >= threshold:
                ball = superball
            else:
                ball = pokeball
            
            # Perform template matching to find the target ball in the screenshot
            result_ball = cv2.matchTemplate(screenshot, ball, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_ball)
            
            # Check again here if the thread should stop
            if stop_event.is_set():
                break

            # If the template matching confidence is above the threshold, click on the image
            if max_val >= threshold:
                # Calculate the coordinates of the top-left corner of the matched region
                top_left = max_loc
                x, y = top_left

                # Calculate the coordinates of the center of the matched region
                height, width, _ = ball.shape
                center_x = x + width // 2
                center_y = y + height // 2

                # Random time to click button
                randomClick = (random.randint(100,300))/100.0
                time.sleep(randomClick)

                # Perform the click using pyautogui
                pyautogui.click(screen.x + center_x, screen.y + center_y)

                if stop_event.is_set():
                    return


    @staticmethod
    def check_captcha():
        while not stop_event.is_set():
            # Load the captcha image
            captcha_image = cv2.imread(path + '\captcha.png')

            # Capture a screenshot of the screen
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

            # Perform template matching to find the captcha image in the screenshot
            result = cv2.matchTemplate(screenshot, captcha_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # If the template matching confidence is above a certain threshold, take appropriate action
            if max_val >= 0.8:
                print('Captcha detected!')
                # Take appropriate action here...

                time.sleep(1)  # check every second or however frequently you want
                print('-------------------------------------------------')
                print('')        
                print(f"      POKEMEOW ASKING FOR CAPTCHA!              ")
                print('')
                print('-------------------------------------------------')
                
                # send a DM using alt account
                header = {
                    'authorization': BOT_TOKEN,
                }
                payload = {
                    'content': "POKEMEOW is asking for CAPTCHA! You have 2 mins to solve!"
                }
                r = requests.post(DM_URL, data=payload, headers=header)

                # shows image
                image = Image.open(path + '\warning.jpg')
                image.show()


                # play beep sound 
                def play_sound(file_path):
                    pygame.mixer.init()
                    pygame.mixer.music.load(file_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(1)

                if __name__ == "__main__":
                    audio_file = os.path.join(path, 'beep.mp3')
                    for i in range(10):
                        play_sound(audio_file)
                        time.sleep(1)
                stop_event.set()
                return


if __name__ == "__main__":
    # Start three threads
    thread1 = threading.Thread(target=pokebot.spawn_pokemon)
    thread2 = threading.Thread(target=pokebot.throw_pokeball)
    thread3 = threading.Thread(target=pokebot.check_captcha)

    # Set threads as daemons
    thread1.daemon = True
    thread2.daemon = True
    thread3.daemon = True

    # Start threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    try:
        while thread1.is_alive() or thread2.is_alive() or thread3.is_alive():
            time.sleep(1)  # wait for 1 second or any suitable time
    except KeyboardInterrupt:
        print("Program stopped by user")
        stop_event.set()
    finally:
        # This is the block of code that will clean up and end the program.
        # Make sure to join all the threads here to ensure they have ended before the main thread ends.
        thread1.join()
        thread2.join()
        thread3.join()
        print("Program has terminated")


