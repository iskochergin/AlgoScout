import os
import re
import csv
import sys


def extract_variants(text):
    variants = []
    pattern = r"^Variant\s+(\d+):\s*$"
    lines = text.splitlines()
    current_id, current_code = None, []
    for line in lines:
        m = re.match(pattern, line)
        if m:
            if current_id is not None:
                variants.append((int(current_id), "\n".join(current_code).rstrip()))
            current_id = m.group(1)
            current_code = []
        else:
            if current_id is not None:
                current_code.append(line)
    if current_id is not None and current_code:
        variants.append((int(current_id), "\n".join(current_code).rstrip()))
    return variants


def generate(OUTPUT_CSV, NUM_CALLS=1):
    sentinel = "END_OF_INPUT"
    print(f"Paste the model output, then on a new line type '{sentinel}' and press Enter:")
    lines = []
    while True:
        line = input()
        if line.strip() == sentinel:
            break
        lines.append(line)
    text = "\n".join(lines)
    variants = extract_variants(text)
    if not variants:
        print("No variants found")
        sys.exit(1)
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["number", "code"])
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for vid, code in variants:
            writer.writerow([vid, code])
    print(f"Saved {len(variants)} variants to '{OUTPUT_CSV}'")
    for vid, code in variants:
        print(f"[Variant {vid}]\n{'-' * 30}\n{code}\n{'-' * 30}")


if __name__ == "__main__":
    OUTPUT_CSV = input("Enter path to output CSV: ").strip()
    generate(OUTPUT_CSV)
