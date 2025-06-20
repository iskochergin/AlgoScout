# AlgoScout
ML powered tool to detect the algorithm by its code

### How to use
0. Clone the repository by 
```bash
git clone https://github.com/iskochergin/AlgoScout
```
1. You need to create a prompt for generating the dataset. 
I prefer generating 75 + 75 versions of code. The **first** generation is more fixed on
different snippet realizations (just function or code without any sort of input, output or variable definition).
The **second** generation is more about creating different configurations with inputs, outputs, variables and 
just some other unusual realizations.

```
Example of these 2 prompts for z-function algorithm:

PROMPT_Z_SNIPPETS = (
    "Generate **10 distinct** Python implementations of the Z-function algorithm (computing the Z-array for a given string). For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No input parsing, no printing, no comments or explanations. **Each snippet must employ a structurally unique approach**—covering both the classic two-pointer/window method and less-common styles (e.g. slicing, generators, recursion, list comprehensions, bitwise tricks, functional constructs). Rename all variables in each variant. Number variants 1–10."
)

PROMPT_Z_IO = (
    "Generate **10 distinct** Python implementations of the Z-function algorithm, each as a complete program. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments or explanations. **Ensure each program is structurally unique**, using different parsing styles, control flows (for vs. while, recursion, comprehension), data structures, or output formatting. Each must include:\n"
    "- variable declarations for the input string (e.g. `s`, `text`, `str_input`) and its length (`n`)\n"
    "- reading the string from stdin\n"
    "- a full `z_function` (or equivalent) routine\n"
    "- computing and printing the Z-array\n"
    "Rename all variables per variant. Number variants 1–10."
)
```

2. Created prompt you put to `dataset/prompts.py`
3. Then you format the `dataset/generate_all.py` to make it matching with your new prompt and algorithm
4. If something went wrong, you may calmly stop the execution of the program and then continue, `progress.json`
stores what the previous execution had stopped on.
5. After the successful execution of `generate_all.py` you are going to have `algo_dataset_preprocessed.csv`. 
Put this file into `model/template` folder where all other files you'll need are stored as well.
6. Configure and run `train.py`. If your code finished with code 0 you'll get `model_skpt` folder. 
7. Success! Now you can simply run `categorize.py` from the same folder with `train.py` and check how it works!

--- 
This repository was created as the ML part of Algolume, which you can find here: [iskochergin/Algolume](https://github.com/iskochergin/Algolume)