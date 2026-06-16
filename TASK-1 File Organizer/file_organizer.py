#importing os ans shutil modules 
import os
import shutil

# Get current folder path
path = os.getcwd()

# Dictionary for file types
folders = {
    ".jpg": "Images",
    ".png": "Images",
    ".txt": "Documents",
    ".pdf": "Documents",
    ".mp3": "Audio"
}

# Read all files
files = os.listdir(path)

for file in files:

    # Skip python file
    if file == "file_organizer.py":
        continue

    # Split file name and extension
    filename, extension = os.path.splitext(file)

    # Check file extension
    if extension in folders:

        folder_name = folders[extension]

        # Create folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        source = os.path.join(path, file)
        destination = os.path.join(path, folder_name, file)

        try:
            shutil.move(source, destination)
            print(f"Moved {file} to {folder_name}")

        except Exception as e:
            print("Error:", e)

    # Delete temporary files
    elif extension == ".tmp":

        try:
            os.remove(file)
            print(f"Deleted {file}")

        except Exception as e:
            print("Error deleting file:", e)