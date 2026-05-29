from faker import Faker
import pandas as pd
import random
import os

fake = Faker()
random.seed(42)

CLAIM_TYPES = ["auto", "home", "life", "renters"]
STATUSES = ["pending", "approved", "denied", "settled"]
US_STATES = ["TX", "IL", "AZ", "GA", "CA", "FL", "NY", "OH"]

def generate_claims(num_claims=5000):
    claims = []
    for i in range(num_claims):
        claims.append({
            "claim_id": f"CLM-{str(i+1).zfill(6)}",
            "policy_number": f"POL-{fake.bothify('??####')}",
            "customer_name": fake.name(),
            "state": random.choice(US_STATES),
            "claim_type": random.choice(CLAIM_TYPES),
            "filed_date": fake.date_between(start_date="-2y", end_date="today"),
            "claim_amount": round(random.uniform(500, 75000), 2),
            "status": random.choice(STATUSES)
        })
    return pd.DataFrame(claims)

os.makedirs("data/raw", exist_ok=True)
df = generate_claims(5000)
df.to_csv("data/raw/claims_raw.csv", index=False)
print(f"Done! Generated {len(df)} claims")
print(df.head())