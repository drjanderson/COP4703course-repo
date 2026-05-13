import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# -----------------------------
# DATABASE CONFIG
# -----------------------------
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),  # psql_db in docker
    port=5432,
    database=os.getenv("POSTGRES_DB"),
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI()

if __name__ == "__main__":
    print("Running manual test")


# -----------------------------
# INIT DATABASE
# -----------------------------
@app.post("/init")
def init_db():
    with engine.begin() as conn:  # auto-commit / rollback
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS accounts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                balance NUMERIC NOT NULL
            )
        """))

        # seed data (safe for lab reset)
        conn.execute(text("DELETE FROM accounts"))

        conn.execute(text("""
            INSERT INTO accounts (name, balance)
            VALUES
                ('Alice', 1000),
                ('Bob', 1000)
        """))

    return {"status": "database initialized"}


# -----------------------------
# GET BALANCE
# -----------------------------
@app.get("/balance/{account_id}")
def get_balance(account_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name, balance FROM accounts WHERE id = :id"),
            {"id": account_id}
        ).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Account not found")

        return {"name": result.name, "balance": float(result.balance)}


# -----------------------------
# TRANSFER MONEY (CORE LAB)
# -----------------------------
@app.post("/transfer")
def transfer(from_id: int, to_id: int, amount: float):

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transfer amount")

    with engine.begin() as conn:
        # Lock both rows to prevent race conditions
        from_account = conn.execute(text("""
            SELECT balance FROM accounts
            WHERE id = :id
            FOR UPDATE
        """), {"id": from_id}).fetchone()

        to_account = conn.execute(text("""
            SELECT balance FROM accounts
            WHERE id = :id
            FOR UPDATE
        """), {"id": to_id}).fetchone()

        if not from_account or not to_account:
            raise HTTPException(status_code=404, detail="Account not found")

        if from_account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # debit sender
        conn.execute(text("""
            UPDATE accounts
            SET balance = balance - :amount
            WHERE id = :id
        """), {"amount": amount, "id": from_id})

        # credit receiver
        conn.execute(text("""
            UPDATE accounts
            SET balance = balance + :amount
            WHERE id = :id
        """), {"amount": amount, "id": to_id})

    return {
        "status": "transfer complete",
        "from": from_id,
        "to": to_id,
        "amount": amount
    }