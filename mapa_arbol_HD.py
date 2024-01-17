import os

def count_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return len(files)

def print_folder_structure_with_file_count(folder_path, indent="", file=None):
    num_files = count_files(folder_path)
    print(f"{indent}{os.path.basename(folder_path)} ({num_files} Archivos)", file=file)

    # List all subdirectories
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Recursively print the structure for each subdirectory
    for subfolder in subfolders:
        print_folder_structure_with_file_count(os.path.join(folder_path, subfolder), indent + "│   ", file=file)

def save_local_structure_to_file(file_path, folder_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        print_folder_structure_with_file_count(folder_path, file=file)

# Replace 'your_folder_path' with the path of the folder you want to visualize
local_folder_path = r'C:\XXXXX\XXXX' #Colocar la ruta de la carpeta de entrada
save_local_structure_to_file('XXXXXXX.txt', local_folder_path) #Ruta y nombre del archivo de salida