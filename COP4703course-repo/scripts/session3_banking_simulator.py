from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
engine = create_engine(
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db",echo=False
)

# -----------------------------------
# CREATE TABLE + SEED DATA
# -----------------------------------
with engine.begin() as conn:

    conn.execute(text("""
        DROP TABLE IF EXISTS accounts
    """))

    conn.execute(text("""
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            balance INT NOT NULL
        )
    """))

    conn.execute(text("""
        INSERT INTO accounts (name, balance)
        VALUES
            ('Alice', 1000),
            ('Bob', 500)
    """))

print("Initial balances created.\n")

# -----------------------------------
# SHOW BALANCES
# -----------------------------------
def show_balances(label):

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT name, balance
            FROM accounts
            ORDER BY id
        """))

        print(label)

        for row in result:
            print(f"{row.name}: ${row.balance}")

        print()


show_balances("=== BEFORE TRANSFER ===")


# -----------------------------------
# BANK TRANSFER SIMULATION
# -----------------------------------
try:

    with Session(engine) as session:

        with session.begin():

            print("Starting transfer...\n")

            # Alice sends $200 to Bob
            session.execute(text("""
                UPDATE accounts
                SET balance = balance - 200
                WHERE name = 'Alice'
            """))

            print("Alice debited $200")

            # -----------------------------------
            # SIMULATED FAILURE
            # -----------------------------------
            raise Exception("Simulated banking system failure!")

            # This never executes
            session.execute(text("""
                UPDATE accounts
                SET balance = balance + 200
                WHERE name = 'Bob'
            """))

            print("Bob credited $200")

except Exception as e:

    print(f"ERROR OCCURRED: {e}")
    print("Transaction rolled back.\n")


# -----------------------------------
# VERIFY BALANCES AFTER FAILURE
# -----------------------------------
show_balances("=== AFTER FAILED TRANSFER ===")