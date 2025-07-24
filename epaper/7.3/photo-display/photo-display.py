import os, sys
import time
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from waveshare_epd import epd7in3f

# Constants
IMG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
EPAPER_WIDTH = 800
EPAPER_HEIGHT = 480
SLIDE_DURATION = 30  # seconds per slide

# Init display
epd = epd7in3f.EPD()
epd.init()

def get_image_files():
    valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
    return [os.path.join(IMG_DIR, f) for f in os.listdir(IMG_DIR) if f.lower().endswith(valid_ext)]

def prepare_image(path):
    img = Image.open(path).convert("RGB")
    # Optional: rotate if image is portrait
    if img.height > img.width:
        img = img.transpose(Image.ROTATE_90)
    # Resize with aspect ratio preserved and white padding
    img = img.resize((EPAPER_WIDTH, EPAPER_HEIGHT), Image.LANCZOS)
    return img

def run_slideshow():
    while True:
        files = get_image_files()
        if not files:
            print("No images found.")
            time.sleep(50)
            continue
        for file_path in files:
            try:
                image = prepare_image(file_path)
                epd.display(epd.getbuffer(image))
                time.sleep(SLIDE_DURATION)
            except Exception as e:
                print(f"Error with {file_path}: {e}")

try:
    run_slideshow()
except KeyboardInterrupt:
    print("Exiting slideshow")
    epd.sleep()