import glob
from PIL import Image

# A4 at 300 DPI
A4_WIDTH, A4_HEIGHT = 2480, 3508

def main():
    # Create blank A4 canvas
    canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    # Load all images from ./images2 folder
    paths = glob.glob("images2/*.*")
    if not paths:
        print("No images found in ./images")
        return

    x, y = 100, 100  # start position
    max_width_per_image = 800  # thumbnail width

    for path in paths:
        img = Image.open(path)
        img.thumbnail((max_width_per_image, max_width_per_image))

        if y + img.height > A4_HEIGHT - 100:
            break  # stop before overflowing

        canvas.paste(img, (x, y))
        y += img.height + 40

    canvas.save("output_A4.png", dpi=(300, 300))
    print("Created output_A4.png")

if __name__ == "__main__":
    main()
