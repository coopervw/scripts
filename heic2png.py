from PIL import Image
import pyheif_pillow_opener

def convert_heic_to_png(heic_file, png_file):
    with Image.open(heic_file) as image:
        image.save(png_file, "PNG")

def convert_folder_images(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".heic"):
            heic_file = os.path.join(folder_path, file_name)
            png_file = os.path.join(folder_path, file_name[:-5] + ".png")
            convert_heic_to_png(heic_file, png_file)
            print(f"Converted: {file_name}")

folder_path = ""
convert_folder_images(folder_path)
