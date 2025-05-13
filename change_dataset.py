import pandas as pd
from preprocess import preprocess_and_canonicalize

df = pd.read_csv("algo_dataset.csv")

df['code'] = df['code'].apply(preprocess_and_canonicalize)

df.to_csv("algo_dataset_preprocessed.csv", index=False)
print("Preprocessed dataset saved to algo_dataset_preprocessed.csv")
