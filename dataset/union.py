import os
import csv

def union(FILES):
    OUTPUT_FILE = "algo_dataset.csv"

    write_header = not os.path.exists(OUTPUT_FILE)

    # Figure out the starting number
    if write_header:
        next_number = 1
    else:
        # Read the last 'number' in the existing file
        with open(OUTPUT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                last_num = int(rows[-1]["number"])
                next_number = last_num + 1
            else:
                next_number = 1

    with open(OUTPUT_FILE, "a", newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        if write_header:
            writer.writerow(["number", "code", "Type"])
        # Append rows from each source file with a global counter
        for filename, alg_type in FILES:
            with open(filename, newline='', encoding='utf-8') as fin:
                reader = csv.DictReader(fin)
                for row in reader:
                    writer.writerow([next_number, row["code"], alg_type])
                    next_number += 1


if __name__ == "__main__":
    from conf import FILES
    union(FILES)
