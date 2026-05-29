import pandas as pd
import psycopg2

conn = psycopg2.connect(host="localhost", port=5433, database="claims_dw", user="engineer", password="statefarmpipeline")
cur = conn.cursor()

df = pd.read_csv("data/processed/claims_clean.csv")
print(f"Loading {len(df)} rows...")

dates = pd.to_datetime(df["filed_date"]).dt.date.unique()
for d in dates:
    cur.execute("INSERT INTO dim_date (full_date, year, quarter, month, month_name) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (full_date) DO NOTHING", (d, d.year, (d.month-1)//3+1, d.month, d.strftime("%B")))
print("dim_date loaded")

policies = df[["policy_number","customer_name","state","claim_type"]].drop_duplicates("policy_number")
for _, row in policies.iterrows():
    cur.execute("INSERT INTO dim_policy (policy_number, customer_name, state, claim_type) VALUES (%s, %s, %s, %s) ON CONFLICT (policy_number) DO NOTHING", (row.policy_number, row.customer_name, row.state, row.claim_type))
print("dim_policy loaded")

cur.execute("SELECT full_date, date_key FROM dim_date")
date_map = {str(r[0]): r[1] for r in cur.fetchall()}
cur.execute("SELECT policy_number, policy_key FROM dim_policy")
policy_map = {r[0]: r[1] for r in cur.fetchall()}

loaded = 0
for _, row in df.iterrows():
    dkey = date_map.get(row["filed_date"])
    pkey = policy_map.get(row["policy_number"])
    if dkey and pkey:
        cur.execute("INSERT INTO fact_claims (claim_id, policy_key, date_key, claim_amount, status, adjuster_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (claim_id) DO NOTHING", (row.claim_id, pkey, dkey, row.claim_amount, row.status, "ADJ-001"))
        loaded += 1

conn.commit()
cur.close()
conn.close()
print(f"fact_claims loaded: {loaded} rows")
print("Warehouse complete!")