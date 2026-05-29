import pytest
import pandas as pd
import sys
sys.path.insert(0, '.')
from ingestion.generate_claims import generate_claims

def test_correct_number_of_claims():
    df = generate_claims(100)
    assert len(df) == 100

def test_required_columns_exist():
    df = generate_claims(10)
    required = ["claim_id", "policy_number", "customer_name", "state", "claim_type", "filed_date", "claim_amount", "status"]
    for col in required:
        assert col in df.columns

def test_claim_amounts_are_positive():
    df = generate_claims(500)
    assert (df["claim_amount"] > 0).all()

def test_status_values_are_valid():
    df = generate_claims(500)
    valid = {"pending", "approved", "denied", "settled"}
    assert set(df["status"].unique()).issubset(valid)

def test_states_are_valid():
    df = generate_claims(500)
    valid = {"TX", "IL", "AZ", "GA", "CA", "FL", "NY", "OH"}
    assert set(df["state"].unique()).issubset(valid)

def test_no_duplicate_claim_ids():
    df = generate_claims(1000)
    assert df["claim_id"].nunique() == len(df)