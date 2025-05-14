import csv

def format_csv(FILES):
    for filename, _ in FILES:
        raw_codes = []
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_codes.append(row["code"])

        rows = []
        for idx, code in enumerate(raw_codes, start=1):
            lines = code.splitlines()
            bad_lines = []
            for i, line in enumerate(lines):
                if "```" in line or not line.strip():
                    print(line)
                    bad_lines.append(i)

            deleted = 0
            for i in bad_lines:
                del lines[i - deleted]
                deleted += 1
            code = "\n".join(lines)

            rows.append({"number": idx, "code": code})

        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["number", "code"])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)


if __name__ == "__main__":
    from conf import FILES
    format_csv(FILES)
