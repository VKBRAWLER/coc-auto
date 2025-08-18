import cv2
import numpy as np
import pyautogui


def screen(template_name):
    """
    Takes a screenshot of the full screen, compares it with a template image,
    and returns the percentage of similarity.
    """
    # Capture screenshot (in memory only)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load template image
    template = cv2.imread(f"{template_name}.png", cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_name}.png' not found.")

    # Template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val * 100  # similarity in %

def compare(img1_path, img2_path):
    """
    Compares two images from disk and returns similarity percentage (0–100).
    Uses template matching.
    """
    img1 = cv2.imread(f"{img1_path}.png", cv2.IMREAD_COLOR)
    img2 = cv2.imread(f"{img2_path}.png", cv2.IMREAD_COLOR)

    if img1 is None:
        raise FileNotFoundError(f"Image not found: {img1_path}")
    if img2 is None:
        raise FileNotFoundError(f"Image not found: {img2_path}")

    # Ensure img1 is bigger than or equal to img2 for template matching
    if img1.shape[0] < img2.shape[0] or img1.shape[1] < img2.shape[1]:
        # Swap if necessary
        img1, img2 = img2, img1

    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val * 100  # similarity in %