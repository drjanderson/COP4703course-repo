# session5_n_plus_one_demo.py
#
# PURPOSE:
# Demonstrate:
#   1. N+1 query problem
#   2. Fix using selectinload
#   3. Performance comparison
#
# RUN:
# docker compose run --rm api python scripts/session5_n_plus_one_demo.py

import os
import time

from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    selectinload
)

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

# ---------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------
Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    echo=True  # IMPORTANT: shows SQL queries
)

Session = sessionmaker(bind=engine)

# ---------------------------------------------------
# Models
# ---------------------------------------------------
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    members = relationship(
        "Member",
        back_populates="team"
    )


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    team_id = Column(
        Integer,
        ForeignKey("teams.id")
    )

    team = relationship(
        "Team",
        back_populates="members"
    )


# ---------------------------------------------------
# Create session
# ---------------------------------------------------
session = Session()

# ===================================================
# PART 1 — N+1 QUERY PROBLEM
# ===================================================
print("\n" + "=" * 60)
print("PART 1 — N+1 QUERY PROBLEM")
print("=" * 60)

start_time = time.perf_counter()

# ONE query here
teams = session.query(Team).all()

# THEN:
# 50 additional queries (roughly)
# one per team when team.members is accessed
for team in teams:

    print(f"\nTEAM: {team.name}")

    # Lazy loading triggers a query EACH TIME
    for member in team.members:
        print(f"   - {member.name}")

end_time = time.perf_counter()

n_plus_one_time = end_time - start_time

print("\n")
print("=" * 60)
print(f"N+1 TOTAL TIME: {n_plus_one_time:.4f} seconds")
print("=" * 60)

# ===================================================
# PART 2 — FIX USING selectinload
# ===================================================
print("\n" + "=" * 60)
print("PART 2 — FIX USING selectinload")
print("=" * 60)

start_time = time.perf_counter()

# SQLAlchemy now performs:
#
# Query 1:
#   Fetch all teams
#
# Query 2:
#   Fetch ALL members for ALL teams
#
# Instead of 51 queries total,
# we now use only 2 queries.
teams = (
    session.query(Team)
    .options(selectinload(Team.members))
    .all()
)

for team in teams:

    print(f"\nTEAM: {team.name}")

    # No additional SQL query here
    for member in team.members:
        print(f"   - {member.name}")

end_time = time.perf_counter()

optimized_time = end_time - start_time

print("\n")
print("=" * 60)
print(f"SELECTINLOAD TOTAL TIME: {optimized_time:.4f} seconds")
print("=" * 60)

# ===================================================
# PART 3 — PERFORMANCE COMPARISON
# ===================================================
print("\n" + "=" * 60)
print("PERFORMANCE COMPARISON")
print("=" * 60)

speedup = n_plus_one_time / optimized_time

print(f"N+1 Query Time:        {n_plus_one_time:.4f} seconds")
print(f"selectinload Time:    {optimized_time:.4f} seconds")
print(f"Speedup:              {speedup:.2f}x faster")

print("=" * 60)

# ---------------------------------------------------
# Cleanup
# ---------------------------------------------------
session.close()