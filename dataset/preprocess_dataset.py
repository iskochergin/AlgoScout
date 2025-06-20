import pandas as pd
from model import preprocess_and_canonicalize


def preprocess_dataset(df):
    df['code'] = df['code'].apply(preprocess_and_canonicalize)

    df.to_csv("algo_dataset_preprocessed.csv", index=False)
    print("Preprocessed dataset saved to algo_dataset_preprocessed.csv")


if __name__ == '__main__':
    df = pd.read_csv("algo_dataset.csv")
    preprocess_dataset(df)