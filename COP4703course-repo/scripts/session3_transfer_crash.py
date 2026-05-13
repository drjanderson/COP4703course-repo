from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db"
)

# -----------------------------
# CREATE TABLE + INIT DATA
# -----------------------------
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS accounts"))

    conn.execute(text("""
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY,
            amount INT
        )
    """))

    conn.execute(text("""
        INSERT INTO accounts (amount) VALUES (100)
    """))

    conn.execute(text("""
        INSERT INTO accounts (amount) VALUES (200)
    """))

# -----------------------------
# SAFE TRANSFER USING session.begin()
# -----------------------------
with Session(engine) as session:
    with session.begin():  # <-- THIS is what you wanted

        session.execute(text("""
            UPDATE accounts
            SET amount = amount - 50
            WHERE id = 1
        """))

        x = 1/0   # Cause a fault

        session.execute(text("""
            UPDATE accounts
            SET amount = amount + 50
            WHERE id = 2
        """))