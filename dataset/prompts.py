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
