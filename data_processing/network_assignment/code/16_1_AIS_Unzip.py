import zipfile
import os

def unzip_files(source_folder, target_folder):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.zip'):
            file_path = os.path.join(source_folder, filename)
            
            # Open and extract the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            print(f'Unzipped: {filename} to {target_folder}')
            
source_folder = r'C:\Users\9hl\Dropbox\ORNL\21.Data\29.MarineCadastre_AIS'  # Replace with your source folder path
target_folder = 'output/16/16_1'  # Replace with your target folder path

unzip_files(source_folder, target_folder)
