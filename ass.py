import pyautogui
import json
import os

LOC_FILE = "loc.json"

def load_locations():
    if os.path.exists(LOC_FILE):
        with open(LOC_FILE, "r") as f:
            return json.load(f)
    return {}

def save_locations(locs):
    with open(LOC_FILE, "w") as f:
        json.dump(locs, f, indent=4)

def assign_location(name):
    input(f"Move your mouse to the '{name}' position and press ENTER...")
    x, y = pyautogui.position()
    locs = load_locations()
    locs[name] = {"x": x, "y": y}
    save_locations(locs)
    print(f"[SAVED] {name} -> x={x}, y={y}")

if __name__ == "__main__":
    while True:
        name = input("Enter a name for location (or 'exit' to quit): ").strip()
        if name.lower() == "exit":
            break
        assign_location(name)
