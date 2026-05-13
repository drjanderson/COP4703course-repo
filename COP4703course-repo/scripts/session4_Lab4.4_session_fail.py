from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import TimeoutError

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
engine = create_engine(

    # Docker service name
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db",

    # Intentionally tiny connection pool
    pool_size=2,
    max_overflow=0,

    # Fail quickly when pool exhausted
    pool_timeout=3,

    echo=True
)

# -------------------------------------------------
# SESSION FACTORY
# -------------------------------------------------
SessionLocal = sessionmaker(bind=engine)

# -------------------------------------------------
# STORE SESSIONS SO THEY NEVER CLOSE
# -------------------------------------------------
sessions = []

print("\nOpening database sessions...\n")

try:

    # Infinite session creation
    for i in range(100):

        print(f"Creating session #{i}")

        session = SessionLocal()

        # Force actual DB connection checkout
        session.execute(text("SELECT 1"))

        # NEVER close session
        sessions.append(session)

        print(f"Session #{i} acquired")

except TimeoutError as e:

    print("\n===================================")
    print("CONNECTION POOL EXHAUSTED")
    print("Application failed.")
    print("===================================\n")

    print(e)

finally:

    print("\nCleaning up sessions...\n")

    for s in sessions:
        s.close()