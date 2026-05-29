import psycopg2

conn = psycopg2.connect(host="localhost", port=5433, database="claims_dw", user="engineer", password="statefarmpipeline")
cur = conn.cursor()

print("=== Total Claims by State ===")
cur.execute("""
    SELECT p.state, COUNT(*) as num_claims, ROUND(AVG(f.claim_amount)::numeric, 2) as avg_claim
    FROM fact_claims f
    JOIN dim_policy p ON f.policy_key = p.policy_key
    GROUP BY p.state
    ORDER BY num_claims DESC
""")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} claims, avg ${row[2]}")

print()
print("=== Claims by Status ===")
cur.execute("""
    SELECT status, COUNT(*) as total
    FROM fact_claims
    GROUP BY status
    ORDER BY total DESC
""")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

print()
print("=== Top 5 Highest Claims ===")
cur.execute("""
    SELECT f.claim_id, p.customer_name, f.claim_amount, f.status
    FROM fact_claims f
    JOIN dim_policy p ON f.policy_key = p.policy_key
    ORDER BY f.claim_amount DESC
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"  {row[0]} | {row[1]} | ${row[2]} | {row[3]}")

cur.close()
conn.close()