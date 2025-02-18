import pandas as pd
import numpy as np
import os


def discretize_numeric(df, col, nbins=5):
    """
    Discretize column 'col' into 'nbins' equi-width bins.
    Each value is replaced with a label of the form: "col_left_right".
    """
    if col not in df.columns:
        return
    col_min = df[col].min()
    col_max = df[col].max()
    # If the column is empty or has NaNs only, skip
    if pd.isna(col_min) or pd.isna(col_max):
        return

    # Create equi-width bin edges
    edges = np.linspace(col_min, col_max, nbins + 1)

    # Use pd.cut to bin the values
    binned = pd.cut(df[col], bins=edges, include_lowest=True, right=False)

    # Convert each bin Interval to a string label
    labels = []
    for iv in binned:
        if pd.isna(iv):
            labels.append(np.nan)
        else:
            left = f"{iv.left:.1f}"
            right = f"{iv.right:.1f}"
            labels.append(f"{col}_{left}_{right}")

    df[col] = labels


if __name__ == "__main__":
    CSV_FILE = "data/bank-data.csv"
    OUTPUT_FIMI_FILE = "input2.txt"

    COLUMNS_TO_REMOVE = ["id"]

    NUMERIC_TO_DISCRETIZE = ["age", "income"]

    N_BINS = 5

    df = pd.read_csv(CSV_FILE)

    df.drop(columns=COLUMNS_TO_REMOVE, inplace=True, errors="ignore")

    for col in NUMERIC_TO_DISCRETIZE:
        discretize_numeric(df, col, nbins=N_BINS)

    transactions = []
    for _, row in df.iterrows():
        items = []
        for col in df.columns:
            val = row[col]
            if pd.notna(val):
                if col in NUMERIC_TO_DISCRETIZE:
                    items.append(str(val))
                else:
                    items.append(f"{col}_{val}")
        transactions.append(items)

    with open(OUTPUT_FIMI_FILE, "w", encoding="utf-8") as f:
        for trans in transactions:
            line = " ".join(trans)
            f.write(line + "\n")


    if os.name == "nt":
        os.system(f".\\apriori -ts -s40 {OUTPUT_FIMI_FILE} output2_sets.txt")
        os.system(f".\\apriori -tr -c90 {OUTPUT_FIMI_FILE} output2_rules.txt")
    else:
        os.system(f"./apriori {OUTPUT_FIMI_FILE} output2.txt")
