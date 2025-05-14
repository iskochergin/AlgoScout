"""
1. Read pre-processed CSV            (algo_dataset_preprocessed.csv)
2. Tokenise with GraphCodeBERT       (microsoft/graphcodebert-base)
3. (Optional) attach graph features  – placeholder included.
4. Fine-tune with Lightning
5. Save model + tokenizer to ./model_ckpt
"""

from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datasets import Dataset
import torch
from torch import nn
import lightning as L
import torchmetrics
from transformers import (AutoTokenizer, AutoModel,
                          get_cosine_schedule_with_warmup)

CSV_PATH = "algo_dataset_preprocessed.csv"
CHECKPOINT_DIR = Path("model_ckpt")
MODEL_NAME = "microsoft/graphcodebert-base"   # 250 M, supports Python

def main():
    # ───────────────────────────── Dataset ────────────────────────────── #
    print("Loading dataset …")
    df = pd.read_csv(CSV_PATH)
    label_enc = LabelEncoder().fit(df["Type"])
    df["label"] = label_enc.transform(df["Type"])
    num_labels = len(label_enc.classes_)
    hf_ds = Dataset.from_pandas(df[["code", "label"]])

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

    def tok_func(ex):
        return tokenizer(
            ex["code"],
            truncation=True,
            padding="max_length",
            max_length=256,  # keeps VRAM moderate
        )

    hf_ds = hf_ds.map(tok_func, batched=True)
    hf_ds.set_format(type="torch",
                     columns=["input_ids", "attention_mask", "label"])

    train_ds = hf_ds.shuffle(seed=42).select(range(int(0.9 * len(hf_ds))))
    val_ds = hf_ds.shuffle(seed=13).select(range(int(0.1 * len(hf_ds))))

    # ───────────────────── Lightning model module ─────────────────────── #
    class AlgoClassifier(L.LightningModule):
        """
        GraphCodeBERT (+ optional GNN) → CLS → MLP
        """

        def __init__(self, n_labels):
            super().__init__()
            self.save_hyperparameters()
            self.encoder = AutoModel.from_pretrained(MODEL_NAME)
            # CLS pooling
            hidden = self.encoder.config.hidden_size
            self.classifier = nn.Sequential(
                nn.Linear(hidden, hidden // 2),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(hidden // 2, n_labels)
            )
            self.criterion = nn.CrossEntropyLoss()
            self.val_acc = torchmetrics.Accuracy(task="multiclass",
                                                 num_classes=n_labels)

        def forward(self, **batch):
            out = self.encoder(**batch)
            cls = out.last_hidden_state[:, 0]  # [CLS]
            return self.classifier(cls)

        def training_step(self, batch, _):
            labels = batch.pop("label")
            logits = self(**batch)
            loss = self.criterion(logits, labels)
            self.log("train_loss", loss, prog_bar=True)
            return loss

        def validation_step(self, batch, _):
            labels = batch.pop("label")
            logits = self(**batch)
            val_loss = self.criterion(logits, labels)
            self.log("val_loss", val_loss, prog_bar=True)
            self.val_acc.update(logits.softmax(-1), labels)

        def on_validation_epoch_end(self):
            self.log("val_acc", self.val_acc.compute(), prog_bar=True)
            self.val_acc.reset()

        def configure_optimizers(self):
            optimizer = torch.optim.AdamW(
                self.parameters(), lr=2e-5, weight_decay=0.01
            )
            steps = len(train_ds) // 8 * 3  # 3 epochs, batch 8
            sched = get_cosine_schedule_with_warmup(
                optimizer, num_warmup_steps=0.1 * steps, num_training_steps=steps
            )
            return [optimizer], [{"scheduler": sched, "interval": "step"}]

    # ───────────────────────────── Training ───────────────────────────── #
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=8,
                                               shuffle=True, num_workers=4)
    val_loader = torch.utils.data.DataLoader(val_ds, batch_size=8,
                                             shuffle=False, num_workers=4)

    model = AlgoClassifier(num_labels)

    trainer = L.Trainer(
        max_epochs=3,
        devices="auto",
        accelerator="auto",
        precision="bf16-mixed" if torch.cuda.is_bf16_supported() else 16,
        gradient_clip_val=1.0,
        log_every_n_steps=10,
    )
    trainer.fit(model, train_loader, val_loader)

    CHECKPOINT_DIR.mkdir(exist_ok=True)
    model.encoder.save_pretrained(CHECKPOINT_DIR)
    tokenizer.save_pretrained(CHECKPOINT_DIR)
    torch.save(model.classifier.state_dict(),
               CHECKPOINT_DIR / "mlp_head.pt")
    label_path = CHECKPOINT_DIR / "labels.txt"
    label_path.write_text("\n".join(label_enc.classes_))
    print(f"✓  Saved model to {CHECKPOINT_DIR.resolve()}")

if __name__ == "__main__":
    torch.multiprocessing.set_start_method("spawn", force=True)
    main()
