import os
import re
import csv
import time
from openai import OpenAI

from prompts import *
from colorama import init, Fore, Style
import sys

init(autoreset=True)


def log_done(msg: str):
    print(Fore.RED + msg)


from conf import API_KEY

MODEL = "google/gemma-3-27b-it:free"

def generate(PROMPT, OUTPUT_CSV, NUM_CALLS=1):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )

    log_done('client done')

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

    # Ensure CSV exists with header
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["number", "code"])

    log_done('variant done')

    for batch in range(NUM_CALLS):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                extra_headers={
                    "HTTP-Referer": "https://yourdomain.com",
                    "X-Title": "10xGenerator"
                },
                messages=[{
                    "role": "user",
                    "content": [{"type": "text", "text": PROMPT}]
                }]
            )
            body = resp.choices[0].message.content
            # print(body)
            variants = extract_variants(body)
            log_done("count snippets: " + str(len(variants)))

            log_done('request done')

            # Append this batch to CSV immediately
            with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for vid, code in variants:
                    number = batch * 10 + vid
                    writer.writerow([number, code])

            log_done('batch done')
            print(f'{batch} BATCH DONE!!!!!!!!!')

            # Print them out
            for vid, code in variants:
                print(f"\n[Batch {batch + 1} Variant {vid}]\n{'-' * 30}\n{code}\n{'-' * 30}")

            time.sleep(3)

        except Exception as e:
            raise e
            print(f"Error on batch {batch + 1}: {e}")
            time.sleep(5)


if __name__ == "__main__":
    OUTPUT_CSV = "algo_datasets/grasshopper_responses.csv"
    generate(PROMPT=PROMPT_DP_GRASSHOPPER, OUTPUT_CSV=OUTPUT_CSV, NUM_CALLS=1)
