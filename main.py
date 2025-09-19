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

def place_troop(char, count=1):
  keyboard.press_and_release(char)
  wait(0.5)
  for i in range(count):
    pyautogui.click(button='left')
  wait(0.5)

def find_attack():
  wait(1)
  mouse_click("attack")
  wait(1)
  mouse_click("find")
  while True:
    wait(2)
    if (screen('cloud') < 60):
      break

def deploy_all(filepath="loc.json"):
  wait(2)
  locs = load_locations(filepath)
  x, y = locs["troop"]["x"], locs["troop"]["y"]
  pyautogui.moveTo(x, y)
  wait(0.2)
  wait(0.2)
  place_troop('1', 7) # super dragon
  place_troop('2', 2) # broom witch
  for key in ["Z", "Q", "W", "E", "R"]: # heros
    place_troop(key)
  wait(0.2)
  keyboard.press_and_release('A')
  wait(0.2)
  for i in range(1, 5):
    px, py = locs['spell' + str(i)]["x"], locs['spell' + str(i)]["y"]
    for _ in range(3):
      pyautogui.click(px, py)
      time.sleep(0.2)

def deploy_one(filepath="loc.json"):
  wait(2)
  keyboard.press_and_release('A')
  wait(0.2)
  locs = load_locations(filepath)
  px, py = locs['spell1']["x"], locs['spell1']["y"]
  pyautogui.click(px, py)
  wait(1)

def exit(instant = None):
  if (instant):
    mouse_click('surrender')
    wait(0.5)
    mouse_click('confirm')
  else:
    while True:
      wait(4)
      if (screen('return') > 60):
        break
  wait(0.5)
  mouse_click("return")
  wait(4)
  
def perform_attacks(n):
  for _ in range(n):
    find_attack()
    notify_sound()
    deploy_all()
    exit()
    notify_sound()

def lose_trophies(n):
  for _ in range(n):
    find_attack()
    deploy_one()
    exit(instant=True)
     

if __name__ == "__main__":
  lose_trophies(30)
  
  # perform_attacks(100)