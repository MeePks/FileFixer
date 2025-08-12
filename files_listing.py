import os
import pandas as pd

filedirectory =rf'Y:\Raw\Retail\GPMI\2025-07-23_DataSet'

file_list = []
for root, dirs, files in os.walk(filedirectory):
    for file in files:
        if file.endswith('.txt'):
            full_path = os.path.join(root, file)
            file_name = file
            file_pattern = file.split('.')[-1]  # Assuming the pattern is the file extension
            file_list.append({'full_path': full_path, 'file_name': file_name, 'file_pattern': file_pattern})

# Create a DataFrame
df = pd.DataFrame(file_list)

df.to_excel(rf'Y:\Raw\Retail\GPMI\2025-07-23_DataSet\file_lists.xlsx', index=False)