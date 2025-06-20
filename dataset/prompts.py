PROMPT_DFS = (
    "Generate **10 distinct** Python implementations of the depth-first search (DFS) algorithm on a directed graph. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments, no explanations, no extra text. Each code snippet must include:\n"
    "- variable declarations (`n`, `m`, `edges`, `s`, `t`)\n"
    "- stdin parsing\n"
    "- a full `dfs` function or equivalent\n"
    "- printing the path or -1\n"
    "Use diverse techniques and rename all variables per variant. Number variants 1–10."
)

PROMPT_DIJKSTRA = (
    "Generate **10 distinct** Python implementations of Dijkstra’s shortest-path algorithm. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments, no explanations, no extra text. Each code snippet must include:\n"
    "- variable declarations (`n`, `m`, `edges`, `src`)\n"
    "- stdin parsing\n"
    "- full algorithm realization (heapq or custom heap)\n"
    "- printing distances and reconstructed paths\n"
    "Use diverse methods and rename all variables per variant. Number variants 1–10."
)

PROMPT_BFS = (
    "Generate **10 distinct** Python implementations of breadth-first search (BFS) for shortest path in an unweighted graph. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments, no explanations, no extra text. Each code snippet must include:\n"
    "- variable declarations (`n`, `m`, `edges`, `s`, `t`)\n"
    "- stdin parsing\n"
    "- full `bfs` function or equivalent\n"
    "- printing hop count and path or -1\n"
    "Use diverse techniques and rename all variables per variant. Number variants 1–10."
)

PROMPT_DP_TURTLE = (
    "Generate **10 distinct** Python implementations of the DP-turtle problem. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments, no explanations, no extra text. Each code snippet must include:\n"
    "- variable declarations (`r`, `c`, `grid`)\n"
    "- stdin parsing\n"
    "- full DP implementation (recursive or iterative)\n"
    "- printing max sum and path string\n"
    "Use diverse methods and rename all variables per variant. Number variants 1–10."
)

PROMPT_DP_GRASSHOPPER = (
    "Generate **10 distinct** Python implementations of the grasshopper DP problem. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments, no explanations, no extra text. Each code snippet must include:\n"
    "- variable declarations (`n`, `route`)\n"
    "- stdin parsing\n"
    "- full DP implementation\n"
    "- printing min cost and visited indices\n"
    "Use diverse methods and rename all variables per variant. Number variants 1–10."
)

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

PROMPT_PREFIX_SNIPPETS = (
    "Generate **10 distinct** Python implementations of the prefix-function (π-array) algorithm. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No I/O handling, no comments or explanations. **Each snippet must use a different structural approach**—from the standard linear scan with backtracking to unusual methods (e.g. slicing windows, recursive computation, generators, decorators, functional style). Rename all variables in each variant. Number variants 1–10."
)

PROMPT_PREFIX_IO = (
    "Generate **10 distinct** Python implementations of the prefix-function algorithm as full programs. For each variant, output exactly:\n"
    "Variant <n>:\n"
    "```python\n"
    "<complete code>\n"
    "```\n"
    "No comments or explanations. **Ensure each program has a unique structure**—varying loop constructs, recursion, slicing, helper functions or classes, and different I/O styles. Each must include:\n"
    "- variable declarations for the input string (e.g. `s`, `pattern`) and its length (`n`)\n"
    "- reading the string from stdin\n"
    "- a complete `prefix_function` (or equivalent) routine\n"
    "- computing and printing the π-array\n"
    "Rename all variables per variant. Number variants 1–10."
)


