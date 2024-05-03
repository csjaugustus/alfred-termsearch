import sys
import os
import pandas as pd
import csv

def strip_empty(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    filtered_rows = []
    for row in rows:
        row_without_empty = [elem for elem in row if elem.strip()]
        filtered_rows.append(row_without_empty)

    with open(csv_path, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerows(filtered_rows)

excel_path = sys.argv[1]
directory = os.path.dirname(excel_path)
file_name = os.path.splitext(os.path.basename(excel_path))[0]
save_path = os.path.join(directory, f"{file_name}.csv")

excel_file = pd.read_excel(excel_path)
excel_file.to_csv(save_path, index=False)
strip_empty(save_path)

sys.stdout.write(save_path)
