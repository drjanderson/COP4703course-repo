"""
PostgreSQL + Docker + SQLAlchemy
N+1 Query Performance Lab
------------------------------------------------

This script assumes:

1. PostgreSQL is running in Docker
2. Database credentials are known
3. SQLAlchemy + psycopg are installed

Install requirements:
------------------------------------------------
pip install sqlalchemy psycopg[binary]

Example Docker command:
------------------------------------------------
docker run --name pg_lab \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=labdb \
    -p 5432:5432 \
    -d postgres:17

Run script:
------------------------------------------------
python n_plus_one_postgres.py
"""

import time

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker,
    selectinload,
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = (
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db"
)

# echo=True prints all generated SQL
engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)


# ============================================================
# BASE CLASS
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# MODELS
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    orders = relationship(
        "Order",
        back_populates="user",
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    item_name = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="orders",
    )


# ============================================================
# RESET DATABASE
# ============================================================

print("\nDropping existing tables...\n")

Base.metadata.drop_all(engine)

print("\nCreating tables...\n")

Base.metadata.create_all(engine)


# ============================================================
# INSERT SAMPLE DATA
# ============================================================

session = SessionLocal()

NUM_USERS = 100
ORDERS_PER_USER = 25

print("\nInserting test data...\n")

for i in range(NUM_USERS):

    user = User(name=f"User_{i}")

    for j in range(ORDERS_PER_USER):

        order = Order(
            item_name=f"Item_{j}"
        )

        user.orders.append(order)

    session.add(user)

session.commit()

print(
    f"\nInserted {NUM_USERS} users "
    f"and {NUM_USERS * ORDERS_PER_USER} orders.\n"
)


# ============================================================
# TEST 1 — N+1 QUERY PROBLEM
# ============================================================

print("\n===================================")
print("TEST 1 — N+1 QUERY PROBLEM")
print("===================================\n")

start = time.perf_counter()

users = session.query(User).all()

total_orders = 0

# Lazy loading triggers
# one additional query per user
for user in users:
    total_orders += len(user.orders)

elapsed = time.perf_counter() - start

print(f"\nTotal orders counted: {total_orders}")
print(f"Elapsed time: {elapsed:.4f} seconds\n")

print("""
EXPECTED RESULT:
----------------
You should see:

1 query:
    SELECT users ...

PLUS many additional queries:
    SELECT orders WHERE user_id = ...

This is the N+1 query problem.
""")


# ============================================================
# TEST 2 — FIX USING selectinload()
# ============================================================

print("\n===================================")
print("TEST 2 — FIX WITH selectinload()")
print("===================================\n")

start = time.perf_counter()

users = (
    session.query(User)
    .options(selectinload(User.orders))
    .all()
)

total_orders = 0

# No extra queries now
for user in users:
    total_orders += len(user.orders)

elapsed = time.perf_counter() - start

print(f"\nTotal orders counted: {total_orders}")
print(f"Elapsed time: {elapsed:.4f} seconds\n")

print("""
EXPECTED RESULT:
----------------
You should now see only:

1 query for users
1 query for all orders using WHERE IN (...)

The N+1 problem is eliminated.
""")


# ============================================================
# CLEANUP
# ============================================================

session.close()

print("\nLab completed successfully.\n")