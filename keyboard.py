import pyautogui
import time

# Writes a certain text on the screen when provided a valid input
def write_text(text):
    if not text:
        return
    pyautogui.write(str(text))

# Presses a certain key and goes through an interval if needed
def press_key(key, interval=0):
    if not key:
        return
    time.sleep(interval)
    pyautogui.press(key)

press_key("a")