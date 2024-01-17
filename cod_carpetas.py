import os
import pandas as pd
import random
import string

def generate_code(folder_name, used_codes, max_attempts=100):
    attempt = 0
    
    while attempt < max_attempts:
        # Take the first two letters from the folder name (or fewer if the name is shorter)
        letters = ''.join(char for char in folder_name[:2].upper() if char.isalpha())
        
        # If the folder name has digits, take the first digit; otherwise, use a random digit
        digit = next((char for char in folder_name if char.isdigit()), str(random.randint(0, 9)))
        
        # Combine the letters and digit to form the code
        code = f'{letters}{digit}'
        
        # Check if the code is valid
        if code not in used_codes and any(char.isdigit() for char in code) and any(char.isalpha() for char in code):
            # Add the code to the list of used codes
            used_codes.add(code)
            return code
        
        attempt += 1
    
    # If max_attempts is reached, generate a unique default code with a random letter instead of "_"
    unique_default_code = f'{random.choice(string.ascii_uppercase)}'
    counter = 2
    while f'{unique_default_code}_{counter}' in used_codes:
        counter += 1
    
    final_default_code = f'{unique_default_code}_{counter}'.replace('_', random.choice(string.ascii_uppercase))
    used_codes.add(final_default_code)
    
    return final_default_code

def create_dataframe(root_folder):
    data = {'Subfolder': [], 'Code': []}
    used_codes = set()
    
    for root, dirs, _ in os.walk(root_folder):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            
            # Generate a code based on the folder name
            code = generate_code(directory, used_codes)
            
            data['Subfolder'].append(directory)
            data['Code'].append(code)

    df = pd.DataFrame(data)
    return df

# Replace 'D:\carpetas a migrar\dummy' with the path to your target folder
folder_path = r'D:\XXXXXXXXXXXXXXXXXX' #carpeta de la cual se sacaran los codigos
result_df = create_dataframe(folder_path)

print(result_df)
#########################################
#Verificar el numero de codigos repetidos
duplicates = result_df['Code'].duplicated()
print(result_df[duplicates])

#########################
#en caso de haber duplicados, este calgoritmo asigna codigos a uno de los duplicados
duplicates = result_df['Code'].duplicated()

for index, is_duplicate in enumerate(duplicates):
    if is_duplicate:
        # Generate a new unique code not already in the DataFrame
        new_code = generate_code(result_df.loc[index, 'Subfolder'], set(result_df['Code']))
        result_df.at[index, 'Code'] = new_code

# Print the modified DataFrame
print(result_df) 