from pathlib import Path
import torch, html
from flask import Flask, render_template, request, redirect, url_for, flash
from model import preprocess
from transformers import AutoTokenizer, AutoModel

CKPT = Path("model_ckpt")
classes  = CKPT.joinpath("labels.txt").read_text().splitlines()
tokenizer = AutoTokenizer.from_pretrained(CKPT)
encoder   = AutoModel.from_pretrained(CKPT)
hidden = encoder.config.hidden_size
mlp = torch.nn.Sequential(
    torch.nn.Linear(hidden, hidden // 2),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.1),
    torch.nn.Linear(hidden // 2, len(classes)),
)
mlp.load_state_dict(torch.load(CKPT / "mlp_head.pt", map_location="cpu"))
encoder.eval(); mlp.eval()

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "replace-me"

# ───────────────────────── helpers ───────────────────────── #

def safe_preprocess(src: str) -> str:
    """Preprocess but never crash on bad input."""
    try:
        return preprocess.preprocess_and_canonicalize(src or "")
    except Exception:
        return src + "\n"

def predict(code: str, top_k: int = 10):
    cleaned = safe_preprocess(code)
    tok = tokenizer(cleaned, truncation=True, padding="max_length",
                    max_length=256, return_tensors="pt")
    with torch.no_grad():
        logits = mlp(encoder(**tok).last_hidden_state[:, 0])
        probs  = torch.softmax(logits, dim=-1).squeeze().tolist()
    ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]

# ───────────────────────── routes ───────────────────────── #

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Prefer uploaded file, else textarea
        code = ""
        if (f := request.files.get("file")) and f.filename:
            code = f.read().decode("utf-8", errors="ignore")
        else:
            code = request.form.get("code", "")
        if not code.strip():
            flash("Please paste code or choose a file first 🙂", "warn")
            return redirect(url_for("index"))
        probs = predict(code)
        return render_template("result.html", probs=probs)
    return render_template("index.html")

if __name__ == "__main__":
    # macOS/Windows spawn safety not needed here but harmless
    torch.multiprocessing.set_start_method("spawn", force=True)
    app.run(debug=False, port=5000)
