import os
import shutil

def move_images(source_folder, destination_folder):
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Ensure the destination folder exists; if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder: {destination_folder}")

    # List all files in the source folder
    files = os.listdir(source_folder)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}  # Common image extensions

    for file_name in files:
        file_path = os.path.join(source_folder, file_name)
        
        # Check if the file is an image
        if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in image_extensions:
            # Move the file to the destination folder
            shutil.move(file_path, os.path.join(destination_folder, file_name))
            print(f"Moved: {file_name}")

    print("All images have been moved.")

# Example usage
source_folder = r"/media/rambo/New Volume/CHTLab/Dataset/Dataset/train"      # Replace with the path to the source folder
destination_folder = r"/media/rambo/New Volume/CHTLab/Dataset/Dataset/train/images"  # Replace with the path to the destination folder
move_images(source_folder, destination_folder)
