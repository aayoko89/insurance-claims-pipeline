import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="claims_dw",
    user="engineer",
    password="statefarmpipeline"
)
cur = conn.cursor()

# Table 1: date information
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_key    SERIAL PRIMARY KEY,
    full_date   DATE UNIQUE NOT NULL,
    year        INT,
    quarter     INT,
    month       INT,
    month_name  VARCHAR(20)
)""")

# Table 2: policy and customer info
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_policy (
    policy_key     SERIAL PRIMARY KEY,
    policy_number  VARCHAR(20) UNIQUE NOT NULL,
    customer_name  VARCHAR(100),
    state          VARCHAR(2),
    claim_type     VARCHAR(20)
)""")

# Table 3: the actual claims
cur.execute("""
CREATE TABLE IF NOT EXISTS fact_claims (
    claim_key      SERIAL PRIMARY KEY,
    claim_id       VARCHAR(20) UNIQUE NOT NULL,
    policy_key     INT REFERENCES dim_policy(policy_key),
    date_key       INT REFERENCES dim_date(date_key),
    claim_amount   NUMERIC(12,2),
    status         VARCHAR(20),
    adjuster_id    VARCHAR(20)
)""")

conn.commit()
cur.close()
conn.close()
print("Tables created successfully!")