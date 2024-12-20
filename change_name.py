import os

def rename_images_in_folder(folder_path, prefix="image", start_index=1):
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # List all files in the folder
    files = os.listdir(folder_path)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}  # Common image extensions
    index = start_index

    for file_name in files:
        # Get full file path
        old_file_path = os.path.join(folder_path, file_name)

        # Skip directories or non-image files
        if not os.path.isfile(old_file_path):
            continue
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension not in image_extensions:
            continue

        # Generate new file name
        new_file_name = f"{prefix}_{index:03}{file_extension}"  # e.g., image_001.jpg
        new_file_path = os.path.join(folder_path, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {file_name} -> {new_file_name}")
        index += 1

    print("Renaming completed.")

# Example usage
folder_path = r"/media/rambo/New Volume/CHTLab/Dataset/Dataset/valid/images"  # Replace with your folder path
rename_images_in_folder(folder_path, prefix="sleeping_position_val", start_index=1)
