import pyautogui
import keyboard
import time
import json
from img import screen
import platform
import os

def notify_sound():
  system = platform.system()

  if system == "Windows":
    import winsound
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)  # Windows notification sound
  elif system == "Darwin":  # macOS
    os.system('afplay /System/Library/Sounds/Glass.aiff')
  else:  # Linux
    os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || echo -n "\a"')

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

def wait(seconds):
  time.sleep(seconds)

def find_attack():
  wait(1)
  mouse_click("attack")
  wait(1)
  mouse_click("find")
  while True:
    wait(2)
    if (screen('cloud') < 60):
      break


def deploy(filepath="loc.json"):
  wait(2)
  locs = load_locations(filepath)
  x, y = locs["troop"]["x"], locs["troop"]["y"]
  pyautogui.moveTo(x, y)
  wait(0.2)
  pyautogui.mouseDown(x, y)
  wait(0.2)
  keyboard.press('1')
  wait(2)
  for key in ["Z", "Q", "W", "E", "R"]:
    keyboard.press(key)
    time.sleep(0.5)
  pyautogui.mouseUp(x, y)
  keyboard.press('A')
  wait(0.2)
  for i in range(1, 5):
    px, py = locs['spell' + str(i)]["x"], locs['spell' + str(i)]["y"]
    for _ in range(3):
      pyautogui.click(px, py)
      time.sleep(0.2)

def exit():
  while True:
    wait(5)
    if (screen('return') > 60):
      break
  keyboard.press('esc')
  wait(7)
  
def perform_attacks(n):
  for _ in range(n):
    find_attack()
    notify_sound()
    deploy()
    exit()
    notify_sound()
  

if __name__ == "__main__":
  perform_attacks(2)