import cv2
import numpy as np
import pyautogui
import time
import requests
import os
import json
import threading
import random
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


class pokebot():
    @staticmethod
    def send_requests():
        data = load_data_from_json()
        TOKEN = data["TOKEN"]
        CHANNEL_URL = data["CHANNEL_URL"]

        while True:
            header = {
                'authorization': TOKEN,
            }
            payload = {
                'content': ";p"
            }

            r = requests.post(CHANNEL_URL, data=payload, headers=header)
            
            randomSleep = (random.randint(1000,1500))/100.0
            print(f"Sleeping for {randomSleep}")
            time.sleep(randomSleep)


    @staticmethod
    def scan_click_button():
        # Specify the index of the screen you want to capture (e.g., 0 for the first screen)
        screen_index = 0

        # Load the target image you want to click on
        p1 = Path(__file__)
        p1 = p1.parent.parent.absolute()
        path = str(p1)
        print(path)
        # target_image = cv2.imread('C:/Users/Santi/Documents/Code/pokebot/script/Pokeball.png')
        target_image = cv2.imread(path + '\Pokeball.png')

        # Get the resolution of the specified screen
        screen = get_monitors()[screen_index]
        screen_width, screen_height = screen.width, screen.height

        while True:
            # Capture a screenshot of the specified screen
            screenshot = pyautogui.screenshot(region=(screen.x, screen.y, screen_width, screen_height))
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

            # Perform template matching to find the target image in the screenshot
            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Specify a threshold for template matching confidence
            threshold = 0.8

            # If the template matching confidence is above the threshold, click on the image
            if max_val >= threshold:
                # Calculate the coordinates of the top-left corner of the matched region
                top_left = max_loc
                x, y = top_left

                # Calculate the coordinates of the center of the matched region
                height, width, _ = target_image.shape
                center_x = x + width // 2
                center_y = y + height // 2

                # Random time to click button
                randomClick = (random.randint(100,300))/100.0
                time.sleep(randomClick)

                # Perform the click using pyautogui
                pyautogui.click(screen.x + center_x, screen.y + center_y)


if __name__ == "__main__":
    # Start two threads
    thread1 = threading.Thread(target=pokebot.send_requests)
    thread2 = threading.Thread(target=pokebot.scan_click_button)

    # Set threads as daemons
    thread1.daemon = True
    thread2.daemon = True

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    try:
        while thread1.is_alive() or thread2.is_alive():
            time.sleep(1)  # wait for 1 second or any suitable time
    except KeyboardInterrupt:
        print("Program stopped by user")

