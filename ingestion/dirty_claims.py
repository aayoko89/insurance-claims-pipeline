import pandas as pd
import random

random.seed(42)

df = pd.read_csv("data/raw/claims_raw.csv")
print(f"Original rows: {len(df)}")

# Add 200 duplicate rows (happens in real systems)
duplicates = df.sample(200)
df = pd.concat([df, duplicates], ignore_index=True)

# Make 150 claim amounts blank (data entry errors)
blank_idx = random.sample(range(len(df)), 150)
df.loc[blank_idx, "claim_amount"] = None

# Add typos in status column (human error)
typo_idx = random.sample(range(len(df)), 100)
df.loc[typo_idx, "status"] = "PNDING"

df.to_csv("data/raw/claims_raw_dirty.csv", index=False)
print(f"Dirty rows: {len(df)}")
print(f"Missing amounts: {df['claim_amount'].isna().sum()}")
print(f"Typos in status: {len(df[df['status'] == 'PNDING'])}")