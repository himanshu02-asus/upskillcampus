"""
File Organizer
--------------
Scans a directory, identifies file types based on their extensions,
and moves them into category folders (Images, Documents, Videos, etc.)

Run:
    python file_organizer.py
    (then enter the folder path you want to organize when prompted)
"""

import os
import shutil

# Map file extensions to category folder names
EXTENSION_MAP = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images", ".webp": "Images",

    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".xlsx": "Documents", ".xls": "Documents",
    ".ppt": "Documents", ".pptx": "Documents", ".csv": "Documents",

    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".wmv": "Videos",

    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".aac": "Audio", ".flac": "Audio",

    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives",

    # Code / scripts
    ".py": "Code", ".java": "Code", ".cpp": "Code", ".html": "Code",
    ".css": "Code", ".js": "Code", ".json": "Code",
}

OTHER_FOLDER = "Others"


def get_category(file_name):
    """Return the category folder name based on the file's extension."""
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    return EXTENSION_MAP.get(ext, OTHER_FOLDER)


def organize_directory(target_dir):
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    moved_count = 0

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        # Skip directories (including any folders we create)
        if os.path.isdir(item_path):
            continue

        category = get_category(item)
        category_path = os.path.join(target_dir, category)

        # Create the category folder if it doesn't exist
        os.makedirs(category_path, exist_ok=True)

        destination = os.path.join(category_path, item)

        # Avoid overwriting files with the same name
        if os.path.exists(destination):
            base, ext = os.path.splitext(item)
            counter = 1
            while os.path.exists(destination):
                destination = os.path.join(category_path, f"{base}_{counter}{ext}")
                counter += 1

        shutil.move(item_path, destination)
        print(f"Moved: {item} -> {category}/")
        moved_count += 1

    if moved_count == 0:
        print("No files to organize. The directory is already tidy!")
    else:
        print(f"\nDone! Organized {moved_count} file(s) in '{target_dir}'.")


if __name__ == "__main__":
    folder = input("Enter the full path of the folder you want to organize: ").strip()
    organize_directory(folder)
