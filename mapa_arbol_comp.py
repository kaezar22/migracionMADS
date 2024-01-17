#Comparar las dos estructuras, de google drive y el backup
def read_structure_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def find_missing_folders(local_structure, drive_structure):
    missing_folders = []
    for line in drive_structure:
        if line not in local_structure:
            missing_folders.append(line.strip())
    return missing_folders

def main():
    # Replace with the paths to your structure files
    local_structure_file = 'arbol_HD.txt' # archivo con el mapa de arbol de la carpeta del disco duro
    drive_structure_file = 'arbol_GD'# archivo con el mapa de arbol de la carpeta de Google Drive

    # Read structure files
    local_structure = read_structure_from_file(local_structure_file)
    drive_structure = read_structure_from_file(drive_structure_file)

    # Find missing folders
    missing_folders = find_missing_folders(local_structure, drive_structure)

    # Print the missing folders
    if missing_folders:
        print("Folders missing in local backup:")
        for folder in missing_folders:
            print(folder)
    else:
        print("No missing folders.")

if __name__ == '__main__':
    main()
