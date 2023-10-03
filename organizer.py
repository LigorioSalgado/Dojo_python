import os
import shutil

source_dir = "/Users/ligorioedwinsalgadoflores/Downloads"

file_extensions = {
    ".pdf" : "pdfs",
    ".jpg" : "Images",
    ".docx" : "Docs",
    ".png" : "Images",
    ".gif" : "Images",
    ".exe" : "Programs",
    ".rar" : "Compress"
}

for filename in os.listdir(source_dir):
    source_file = os.path.join(source_dir, filename)

    if os.path.isfile(source_file):
        extension = os.path.splitext(filename)[1]
        destination_folder = file_extensions.get(extension,"Stuff")

        destination_directory = os.path.join(source_dir, destination_folder)
        os.makedirs(destination_directory, exist_ok=True)

        destination_file = os.path.join(destination_directory, filename)
        shutil.move(source_file, destination_file)
        print(f"Moved: {filename} to {destination_folder}")


