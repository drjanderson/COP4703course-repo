import time
import psycopg2
from psycopg2 import extras

# -----------------------------
# DB CONNECTION (Docker case)
# -----------------------------
conn = psycopg2.connect(
    dbname="my_db",
    user="admin",
    password="mysecretpassword",
    host="localhost",   # use "db" if running inside docker-compose network
    port="5432"
)

cur = conn.cursor()

# -----------------------------
# CREATE TABLE
# -----------------------------
cur.execute("""
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL
);
""")
conn.commit()

# -----------------------------
# DATA GENERATION
# -----------------------------
NUM_ROWS = 10_000
data = [(f"user_{i}",) for i in range(NUM_ROWS)]

# =========================================================
# 1. executemany()
# =========================================================
start = time.time()

cur.executemany(
    "INSERT INTO users (username) VALUES (%s)",
    data
)

conn.commit()
execmany_time = time.time() - start

# Clear table for next test
cur.execute("TRUNCATE TABLE users;")
conn.commit()

# =========================================================
# 2. execute_values() (FAST METHOD)
# =========================================================
start = time.time()

extras.execute_values(
    cur,
    "INSERT INTO users (username) VALUES %s",
    data
)

conn.commit()
execute_values_time = time.time() - start

# -----------------------------
# RESULTS
# -----------------------------
print("\n===== PERFORMANCE RESULTS =====")
print(f"executemany() time:      {execmany_time:.4f} seconds")
print(f"execute_values() time:    {execute_values_time:.4f} seconds")

# Cleanup
cur.close()
conn.close()