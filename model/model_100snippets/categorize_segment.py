from pathlib import Path
import torch
from flask import Flask, render_template, request, redirect, url_for, flash
import preprocess                     # your robust pre-processor
from transformers import AutoTokenizer, AutoModel

# ──────────────────── Load Model & Tokenizer ────────────────────── #
CKPT = Path("model_ckpt")
classes  = CKPT.joinpath("labels.txt").read_text().splitlines()
tokenizer = AutoTokenizer.from_pretrained(CKPT)
encoder   = AutoModel.from_pretrained(CKPT).eval()
hidden = encoder.config.hidden_size
mlp = torch.nn.Sequential(
    torch.nn.Linear(hidden, hidden // 2),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.1),
    torch.nn.Linear(hidden // 2, len(classes)),
)
mlp.load_state_dict(torch.load(CKPT / "mlp_head.pt", map_location="cpu"))
mlp.eval()

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "replace-me"

# ─────────────────────────── Helpers ────────────────────────────── #

def safe_preprocess(src: str) -> str:
    """Never raise, even on malformed code."""
    try:
        return preprocess.preprocess_and_canonicalize(src or "")
    except Exception:
        return src + "\n"

@torch.no_grad()
def classify_snippets(snippets: list[str]) -> torch.Tensor:
    """
    Batch-tokenize & classify a list of code snippets.
    Returns tensor of shape [len(snippets), num_classes] with softmax probs.
    """
    toks = tokenizer(
        snippets,
        truncation=True,
        padding="longest",
        max_length=256,
        return_tensors="pt"
    )
    out = encoder(**toks).last_hidden_state[:, 0]  # CLS
    logits = mlp(out)
    return torch.softmax(logits, dim=-1)

def predict_fast(code: str, top_k: int = 5, conf_thresh: float = 0.8):
    """
    1) Classify full snippet; if top-prob ≥ conf_thresh, return immediately.
    2) Otherwise run a batched sliding-window scan, take max over windows.
    """
    lines = code.splitlines()
    n = len(lines)

    # 1) Full-snippet pass
    full = safe_preprocess(code)
    full_probs = classify_snippets([full])[0]
    # if super-confident, skip windows
    if full_probs.max() >= conf_thresh:
        ranked = sorted(
            zip(classes, full_probs.tolist()),
            key=lambda x: x[1], reverse=True
        )
        return ranked[:top_k]

    # 2) Windowed pass
    windows = []
    window_sizes = [5, 10, 20]         # try small, medium, larger contexts
    if len(lines) > 50:
        window_sizes = [20]
    for w in window_sizes:
        for i in range(0, n - w + 1):
            j = min(i + w, n)
            snippet = "\n".join(lines[i:j]).strip()
            windows.append(safe_preprocess(snippet))

    # Batch in chunks
    max_probs = torch.zeros(len(classes))
    batch_size = 16
    for i in range(0, len(windows), batch_size):
        batch = windows[i : i + batch_size]
        probs = classify_snippets(batch)       # shape [b, C]
        max_probs = torch.maximum(max_probs, probs.max(dim=0).values)

    # Merge full-snippet too
    max_probs = torch.maximum(max_probs, full_probs)

    ranked = sorted(
        zip(classes, max_probs.tolist()),
        key=lambda x: x[1], reverse=True
    )
    return ranked[:top_k]

# ─────────────────────────── Routes ────────────────────────────── #

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = ""
        f = request.files.get("file")
        if f and f.filename:
            code = f.read().decode("utf-8", errors="ignore")
        else:
            code = request.form.get("code", "")

        if not code.strip():
            flash("Please paste code or choose a file first 🙂", "warn")
            return redirect(url_for("index"))

        results = predict_fast(code, top_k=5, conf_thresh=0.75)
        return render_template("result.html", probs=results)

    return render_template("index.html")

if __name__ == "__main__":
    torch.multiprocessing.set_start_method("spawn", force=True)
    app.run(debug=False, port=5000)
