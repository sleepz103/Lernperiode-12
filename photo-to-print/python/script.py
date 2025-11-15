from PIL import Image
import glob

# Create A4 at 300 DPI
a4_width, a4_height = 2480, 3508  # pixels
canvas = Image.new("RGB", (a4_width, a4_height), "white")

# Load image folder
imgs = glob.glob("./images2/*.jpg") + glob.glob("./images2/*.png")

x, y = 100, 100
for path in imgs:
    img = Image.open(path)
    img.thumbnail((800, 800))
    canvas.paste(img, (x, y))
    y += img.height + 50

canvas.save("layout.png", dpi=(300, 300))
