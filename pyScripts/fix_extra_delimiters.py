import os
import csv

input_directory = rf'Y:\Split\Retail\GPMI\202507-23_DataSet\test'  # Update this path
expected_delimiters = None  # Set to None to auto-detect based on the first valid line
delimeter = '|'  # Change this to your expected delimiter
delimeter_postion_to_replace=47 -1

def detect_line_ending(sample):
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.lineterminator
    except Exception:
        return '\r\n'
    


for filename in os.listdir(input_directory):
    if(filename.endswith('invoices_2024_GPMI.txt')):
        expected_delimiters = None
        input_path= os.path.join(input_directory, filename)
        print(f"Processing file: {input_path}")
        ouptut_path = os.path.join(input_directory, filename.replace('.txt', '_fixed.txt'))
        log_file_path = os.path.join(input_directory, f'processing_log_{filename}.tf.err')

        cnt_row=0

        with open(input_path, 'r', encoding='utf-8', newline='') as file,open(ouptut_path,'w', encoding='utf-8-sig' ,newline='') as output_file:
            sample = file.read(5000)
            line_ending=detect_line_ending(sample)
            file.seek(0)
            for line in file:
                cnt_row += 1
                line =line.strip()

                if not line: 
                    continue

                if expected_delimiters is None and delimeter in line:
                    expected_delimiters = line.count(delimeter)
                    print(f"Expected delimiters in {filename}: {expected_delimiters}")
                    with open(log_file_path, 'a', encoding='utf-8') as log_file:
                        log_file.write(f"Expected Delimeters: {expected_delimiters} \n")

                current_delimiters = line.count(delimeter)

                if current_delimiters>expected_delimiters:
                    print(f"Row {cnt_row} has more delimiters than expected: {current_delimiters} vs {expected_delimiters}")
                    with open(log_file_path, 'a', encoding='utf-8') as log_file:
                        log_file.write(f"Row {cnt_row}:: Delimeters {current_delimiters} ::  {line}\n")
                    parts = line.split(delimeter)
                    while(current_delimiters>expected_delimiters):
                        parts[delimeter_postion_to_replace]=parts[delimeter_postion_to_replace]+ parts[delimeter_postion_to_replace + 1]
                        del parts[delimeter_postion_to_replace + 1]
                        fixed_line = delimeter.join(parts)
                        current_delimiters = fixed_line.count(delimeter)
                    output_file.write(fixed_line + line_ending)
                else:
                    output_file.write(line + line_ending)


                