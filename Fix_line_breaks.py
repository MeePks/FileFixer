import os
import csv



#--- Configurations ----

input_directory = rf"Y:\Split\Retail\GPMI\202507-23_DataSet\InvoicesGPMI"
expected_delimiters = None
delimeter= "|"


def detect_line_ending(sample: str) -> str:
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.lineterminator
    except Exception:
        return '\r\n'

for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_directory, filename)
        print(f"Processing file: {input_path}")
        output_path = os.path.join(input_directory,filename.replace('.txt', '_fixed.txt'))
        log_file_path = os.path.join(input_directory, f'processing_log_{filename}.tf.err')

        
        strline=""
        concat_status = False
        concat_row=0
        altered_rows=[]
        output_lines = []
        cnt_row=0

        with open(input_path, 'r', encoding='utf-8', newline='') as file:
            sample = file.read(5000)  # Read a sample to detect line endings
            line_ending =detect_line_ending(sample)
            print(line_ending)
            file.seek(0)
            for line in file:
                cnt_row+=1
                #print(f"Processing row {cnt_row}: {line.strip()} ")
                print(f"Processing row {cnt_row}... ", end='')
                line = line.strip()

                if not line: 
                    continue

                if expected_delimiters is None and delimeter in line:
                    expected_delimiters=line.count(delimeter)
                    #print(f"Expected delimiters in {filename}: {expected_delimiters}")

                current_delimiters = line.count(delimeter)
                #print(f"Current delimiters in row {cnt_row}: {current_delimiters}")

                if current_delimiters ==expected_delimiters and not concat_status:
                    output_lines.append(line)

                elif current_delimiters< expected_delimiters and not concat_status:
                    strline = line
                    concat_status = True
                    altered_rows.append(cnt_row)

                elif concat_status:
                    strline+=line
                    merged_delims =strline.count(delimeter)
                    if merged_delims == expected_delimiters:
                        output_lines.append(strline)
                        concat_status = False
                    else:
                        altered_rows.append(cnt_row)
                
                elif current_delimiters > expected_delimiters:
                    with open(log_file_path, 'a') as log_file:
                        log_file.write(f"Warning: Row {cnt_row}  has more delimiters than expected ({current_delimiters} vs {expected_delimiters}). Skipping this row.\n")
                        #print(f"Warning: Row {cnt_row}  has more delimiters than expected ({current_delimiters} vs {expected_delimiters}). Skipping this row.")
                    output_lines.append(line)

        with open(output_path, 'w' , encoding='utf-8-sig' ,newline='') as output_file:
            for line in output_lines:
                output_file.write(line + line_ending )

        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Processed file: {filename}\n")
            log_file.write(f"Input rows: {cnt_row}\n")
            log_file.write(f"Output rows: {len(output_lines)}\n")
            log_file.write(f"Altered row numbers: {altered_rows if altered_rows else 'None'}\n")
            log_file.write(f"Output file: {output_path}\n")
            log_file.write("-" * 50 + "\n")



        print(f"\n[{filename}] PROCESSING SUMMARY")
        print(f"  Input rows         : {cnt_row}")
        print(f"  Output rows        : {len(output_lines)}")
        print(f"  Altered row numbers: {altered_rows if altered_rows else 'None'}")
        print(f"  Output file        : {output_path}")
        print("-" * 50)
