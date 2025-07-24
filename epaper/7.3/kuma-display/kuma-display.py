import os, time
from PIL import Image, ImageOps, ImageFont
# from waveshare_epd import epd7in3f  # Use your exact model
import logging

logging.basicConfig(level=logging.DEBUG)

# Pic Dir
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

# --- CONFIGURATION ---
URL = "https://kuma.nstudios.dev/status/services"

IMG_PATH = os.path.join(picdir, "screenshot.png")
OUTPUT_PATH = os.path.join(picdir, "kuma-epaper.png")

EPAPER_WIDTH = 800
EPAPER_HEIGHT = 480

CROP_TOP = 200
CROP_BOTTOM = 80
CROP_LEFT = 40
CROP_RIGHT = 40

start_time = time.time()

# --- Step 1: Take screenshot ---
logging.info("Taking screenshot...")
os.system(f"chromium-browser --headless --disable-gpu --window-size=780,1440 --force-device-scale-factor=2 --screenshot={IMG_PATH} {URL}")
time.sleep(3)  # wait for screenshot to be saved

# # --- Step 2: Open and convert screenshot ---
logging.info("Processing image...")

image = Image.open(IMG_PATH)

# Crop to focus on main content
cropped = image.crop((
    CROP_LEFT,
    CROP_TOP,
    image.width - CROP_RIGHT,
    image.height - CROP_BOTTOM
))

# # Rotate 90 degrees clockwise (transpose keeps metadata clean)
# rotated = cropped.transpose(Image.ROTATE_90)


# # Maintain aspect ratio, add letterbox if needed
# # resized = ImageOps.pad(cropped, (EPAPER_WIDTH, EPAPER_HEIGHT), color='white', method=Image.LANCZOS)

# # # Resize to e-paper resolution
# resized = rotated.resize((EPAPER_WIDTH, EPAPER_HEIGHT), Image.LANCZOS)

cropped.save(OUTPUT_PATH, dpi=(72, 72))

# # Save as BMP (for Waveshare)
# resized.save(f"{picdir}/kuma-epaper.bmp", format="BMP", dpi=(72, 72))

# # --- Step 3: Send to e-paper display ---
# logging.info("Displaying on e-paper...")
# epd = epd7in3f.EPD()
# epd.init()
# # epd.Clear()

# # Font
# font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
# font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
# font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)

# epd.display(epd.getbuffer(resized))
# epd.sleep()

# # --- Done ---
# elapsed = time.time() - start_time