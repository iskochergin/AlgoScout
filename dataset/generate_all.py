import os
import json
from generate import generate
from prompts import *
from conf import FILES
import pandas as pd
import generate_input

PROGRESS_FILE = "progress.json"

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        data = json.load(f)
        start_i = data.get("prompt_index", 0)
else:
    start_i = 0

# here put your own prompts (stored in prompts.py)
prompts_list = [PROMPT_DP_GRASSHOPPER, PROMPT_DP_TURTLE, PROMPT_DFS, PROMPT_BFS, PROMPT_DIJKSTRA, PROMPT_Z_IO,
                PROMPT_PREFIX_IO]

for i in range(start_i, len(prompts_list)):
    PROMPT = prompts_list[i]
    OUTPUT = FILES[i][0]

    print("Generating " + OUTPUT)
    print()
    print("PROMPT: " + PROMPT)
    print()
    generate(PROMPT=PROMPT, OUTPUT_CSV=OUTPUT, NUM_CALLS=8)

    # --- save progress after each prompt ---
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"prompt_index": i + 1}, f)

    cont = input("Continue? [y/n] ")
    if cont != "y":
        exit(0)

print("generating finished successfully")
print("turning to formating datasets")

cont = input("Continue? [y/n] ")
if cont != "y":
    exit(0)

from format_csv import format_csv

format_csv(FILES=FILES)
print("formatting finished successfully")
print("turning to union datasets")

cont = input("Continue? [y/n] ")
if cont != "y":
    exit(0)

from union import union

union(FILES=FILES)
print("union finished successfully")
print("turning to preprocess dataset")

cont = input("Continue? [y/n] ")
if cont != "y":
    exit(0)

from preprocess_dataset import preprocess_dataset

preprocess_dataset(df=pd.read_csv("algo_dataset.csv"))
print("preprocess finished successfully")
print("all done!")
