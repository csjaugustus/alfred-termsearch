import sys
import os
import json
import csv

# excel_file = pd.read_excel('/Users/augustuschen/Desktop/Book1.xlsx')
# excel_file.to_csv('output_file.csv', index=False)

csv_path = os.environ["csv_path"]
save_file_name = os.environ["save_file_name"]
termbase_dir = os.environ["termbase_dir"]
d = {}

with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        d[row[0]] = row[1:]

save_path = os.path.join(termbase_dir, f"{save_file_name}.json")

with open(save_path, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=4, ensure_ascii=False)

sys.stdout.write(f'Successfully loaded "{os.path.basename(csv_path)}".')
