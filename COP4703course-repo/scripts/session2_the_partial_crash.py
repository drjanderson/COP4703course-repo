import psycopg2

DB_URI = "dbname=my_db user=admin password=mysecretpassword host=psql_db port=5432"

# -------------------------
# PART 1: SUCCESSFUL LOAD
# -------------------------
with psycopg2.connect(DB_URI) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS demo_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            );
        """)

        cur.execute("""
            INSERT INTO demo_users (name)
            VALUES ('Alice'), ('Bob'), ('Charlie');
        """)

    # explicit commit (safe demonstration)
    conn.commit()

print("Part 1 committed successfully")


# -------------------------
# PART 2: FAILED LOAD
# -------------------------
try:
    with psycopg2.connect(DB_URI) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO demo_users (name)
                VALUES ('David'), ('Eve');
            """)

            # FORCE ERROR (simulates bug)
            x = 1 / 0

            cur.execute("""
                INSERT INTO demo_users (name)
                VALUES ('Frank');
            """)

        conn.commit()

except Exception as e:
    print("ERROR occurred:", e)
    print("Second transaction rolled back automatically")

print("Done")