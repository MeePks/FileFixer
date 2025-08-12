import os
import pandas as pd

def detect_headers(directory):
    headers = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'): 
            with open(os.path.join(directory, filename), 'r') as file:
                first_line = file.readline().strip()
                headers[filename] = first_line.split('|')
                df = pd.DataFrame([[filename] + headers[filename]])
                df.to_csv('headers.csv', mode='a', header=False, index=False)


if __name__ == "__main__":
    directory_path = rf'Y:\Raw\Retail\GPMI\2025-07-23_DataSet'
    headers = detect_headers(directory_path)
    







