import pyautogui
import time
import json
import screen from img

# Load locations
def load_locations(filepath="loc.json"):
    with open(filepath, "r") as f:
        return json.load(f)

# Mouse functions
def mouse_click(name, button="left", filepath="loc.json"):
    """
    Click at the location stored with the given name.
    Example: mouse_click("start")
    """
    locs = load_locations(filepath)
    if name not in locs:
        print(f"[ERROR] '{name}' not found in {filepath}")
        return
    x, y = locs[name]["x"], locs[name]["y"]
    pyautogui.click(x=x, y=y, button=button)

def mouse_long_press(name, duration=1.0, button="left", filepath="loc.json"):
    """
    Long press at a saved location.
    """
    locs = load_locations(filepath)
    if name not in locs:
        print(f"[ERROR] '{name}' not found in {filepath}")
        return
    x, y = locs[name]["x"], locs[name]["y"]
    pyautogui.mouseDown(x=x, y=y, button=button)
    time.sleep(duration)
    pyautogui.mouseUp(x=x, y=y, button=button)

def key_press(key):
    pyautogui.press(key)

def wait(seconds):
    time.sleep(seconds)

def find_attack():
    mouse_click("attack")
    wait(1)
    mouse_click("find")
    while True:
        wait(3)
        if (img('cloud') < 90):
            break

if __name__ == "__main__":
    print("Automation script will run in 3 seconds...")
    time.sleep(3)
    perform_actions()
