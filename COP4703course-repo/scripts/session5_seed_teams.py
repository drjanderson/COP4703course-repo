# seed_teams.py

import random
import os

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
    sessionmaker
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

print("Connecting to database...")

# ---------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------
Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Session = sessionmaker(bind=engine)
session = Session()

# ---------------------------------------------------
# Models
# ---------------------------------------------------
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        nullable=False,
        unique=True
    )

    members = relationship(
        "Member",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Team(name={self.name})>"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        nullable=False
    )

    team_id = Column(
        Integer,
        ForeignKey("teams.id")
    )

    team = relationship(
        "Team",
        back_populates="members"
    )

    def __repr__(self):
        return f"<Member(name={self.name})>"


# ---------------------------------------------------
# Create tables
# ---------------------------------------------------
print("Creating tables...")

Base.metadata.create_all(engine)

# ---------------------------------------------------
# Team names
# ---------------------------------------------------
team_names = [
    "Lions", "Tigers", "Bears", "Hawks", "Wolves",
    "Panthers", "Sharks", "Falcons", "Dragons", "Knights",
    "Storm", "Thunder", "Cyclones", "Titans", "Raiders",
    "Warriors", "Pirates", "Rangers", "Spartans", "Bulldogs",
    "Eagles", "Coyotes", "Vikings", "Comets", "Phoenix",
    "Jets", "Rhinos", "Mustangs", "Cobras", "Hornets",
    "Kings", "Giants", "Pioneers", "Blazers", "Rebels",
    "Stars", "Heat", "Lightning", "Wildcats", "Bruins",
    "Gators", "Foxes", "Owls", "Grizzlies", "Scorpions",
    "Stallions", "Barracudas", "Rockets", "Avalanche", "Inferno"
]

# ---------------------------------------------------
# Member name data
# ---------------------------------------------------
first_names = [
    "Alice", "Bob", "Charlie", "David", "Emma",
    "Frank", "Grace", "Henry", "Isabella", "Jack",
    "Karen", "Liam", "Mia", "Nathan", "Olivia",
    "Paul", "Quinn", "Ryan", "Sophia", "Tyler",
    "Uma", "Victor", "William", "Xavier", "Yara",
    "Zach"
]

last_names = [
    "Smith", "Johnson", "Brown", "Taylor", "Anderson",
    "Thomas", "Jackson", "White", "Harris", "Martin"
]

# ---------------------------------------------------
# Clear old data
# ---------------------------------------------------
print("Deleting old data...")

session.query(Member).delete()
session.query(Team).delete()

session.commit()

# ---------------------------------------------------
# Insert teams and members
# ---------------------------------------------------
print("Seeding database...")

for team_name in team_names:

    team = Team(name=team_name)

    # Random number of members: 1-10
    member_count = random.randint(1, 10)

    for _ in range(member_count):

        full_name = (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        )

        member = Member(name=full_name)

        team.members.append(member)

    session.add(team)

# ---------------------------------------------------
# Save to database
# ---------------------------------------------------
session.commit()

print("Database seeded successfully!")

# ---------------------------------------------------
# Display teams and members
# ---------------------------------------------------
teams = session.query(Team).all()

for team in teams:

    print(f"\n{team.name}")

    for member in team.members:
        print(f"   - {member.name}")