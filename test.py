import cv2
import numpy as np
import pyautogui
import time
import os

def _timestamped_filename(prefix, ext="png"):
    """Generate a timestamped filename inside debug/ folder."""
    os.makedirs("debug", exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join("debug", f"{prefix}_{timestamp}.{ext}")

def screen(template_name, save_debug=True):
    """
    Takes a screenshot of the full screen, compares it with a template image,
    and returns the percentage of similarity.
    Optionally saves a debug image with similarity % text.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(f"{template_name}.png", cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_name}.png' not found.")

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    similarity = max_val * 100

    if save_debug:
        h, w = template.shape[:2]
        cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
        # Top-left corner text
        cv2.putText(screenshot, f"{similarity:.2f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        filename = _timestamped_filename(f"debug_{template_name}")
        cv2.imwrite(filename, screenshot)

    return similarity


def compare(img1_path, img2_path, save_debug=True):
    """
    Compares two images from disk and returns similarity percentage (0–100).
    Uses template matching. Saves a debug image with similarity % text.
    """
    img1 = cv2.imread(f"{img1_path}.png", cv2.IMREAD_COLOR)
    img2 = cv2.imread(f"{img2_path}.png", cv2.IMREAD_COLOR)

    if img1 is None:
        raise FileNotFoundError(f"Image not found: {img1_path}.png")
    if img2 is None:
        raise FileNotFoundError(f"Image not found: {img2_path}.png")

    if img1.shape[0] < img2.shape[0] or img1.shape[1] < img2.shape[1]:
        img1, img2 = img2, img1

    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    similarity = max_val * 100

    if save_debug:
        h, w = img2.shape[:2]
        cv2.rectangle(img1, max_loc, (max_loc[0] + w, max_loc[1] + h), (255, 0, 0), 2)
        cv2.putText(img1, f"{similarity:.2f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        filename = _timestamped_filename("debug_compare")
        cv2.imwrite(filename, img1)

    return similarity


def run_for_seconds(template_name, duration=7, interval=1):
    """
    Continuously runs screen(template_name) for `duration` seconds.
    Captures similarity every `interval` seconds.
    """
    print(f"Running screen('{template_name}') for {duration} seconds...")
    start = time.time()
    while time.time() - start < duration:
        similarity = screen(template_name, save_debug=True)
        print(f"Similarity: {similarity:.2f}%")
        time.sleep(interval)
    print("✅ Finished running.")

# run_for_seconds("cloud", duration=7, interval=0.5)

from img import compare
time.sleep(1)
print(compare('image', 'return'))