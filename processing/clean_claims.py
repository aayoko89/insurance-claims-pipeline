import pandas as pd
import os

# Load the dirty data
df = pd.read_csv("data/raw/claims_raw_dirty.csv")
print(f"Dirty rows loaded: {len(df)}")

# Fix 1: Remove duplicate rows
df = df.drop_duplicates()
print(f"After removing duplicates: {len(df)}")

# Fix 2: Fill missing claim amounts with the average
avg = df["claim_amount"].mean()
df["claim_amount"] = df["claim_amount"].fillna(round(avg, 2))
print(f"Missing amounts fixed with average: ${round(avg, 2)}")

# Fix 3: Fix the PNDING typo
df["status"] = df["status"].replace("PNDING", "pending")
print(f"Typos fixed")

# Add a loss ratio column
df["loss_ratio"] = 0.0

# Save the clean data
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/claims_clean.csv", index=False)
print(f"Clean data saved!")
print(f"Final row count: {len(df)}")
print(df.head())