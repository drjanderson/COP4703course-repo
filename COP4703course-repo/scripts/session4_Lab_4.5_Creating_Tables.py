from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)

from sqlalchemy.sql import func


# =========================================================
# DATABASE CONNECTION
# =========================================================
engine = create_engine(
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db",
    echo=True
)

SessionLocal = sessionmaker(bind=engine)


# =========================================================
# BASE CLASS
# =========================================================
class Base(DeclarativeBase):
    pass


# =========================================================
# TIMESTAMP MIXIN
# =========================================================
class TimestampMixin:

    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# =========================================================
# USERS TABLE
# =========================================================
class User(TimestampMixin, Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    # Refuse incomplete data
    name = Column(String, nullable=False)

    # Refuse incomplete data
    email = Column(String, nullable=False, unique=True)


# =========================================================
# TEAMS TABLE
# =========================================================
class Team(TimestampMixin, Base):

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    # Refuse incomplete data
    name = Column(String, nullable=False)


# =========================================================
# ENROLLMENTS TABLE
# =========================================================
class Enrollment(TimestampMixin, Base):

    __tablename__ = "enrollments"

    # Composite Primary Key
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False
    )

    team_id = Column(
        Integer,
        ForeignKey("teams.id"),
        primary_key=True,
        nullable=False
    )

    # Refuse incomplete data
    role = Column(String, nullable=False)


# =========================================================
# DROP OLD TABLES (OPTIONAL FOR TESTING)
# =========================================================
Base.metadata.drop_all(bind=engine)


# =========================================================
# CREATE TABLES
# =========================================================
Base.metadata.create_all(bind=engine)


# =========================================================
# INSERT SAMPLE DATA
# =========================================================
with SessionLocal() as session:

    # -----------------------------
    # Insert User
    # -----------------------------
    alice = User(
        name="Alice",
        email="alice@example.com"
    )

    session.add(alice)

    # -----------------------------
    # Insert Team
    # -----------------------------
    dev_team = Team(
        name="Development"
    )

    session.add(dev_team)

    # Flush required so IDs exist
    session.flush()

    # -----------------------------
    # Insert Enrollment
    # -----------------------------
    enrollment = Enrollment(
        user_id=alice.id,
        team_id=dev_team.id,
        role="Developer"
    )

    session.add(enrollment)

    # Commit transaction
    session.commit()


# =========================================================
# PRINT USERS
# =========================================================
with SessionLocal() as session:

    print("\n=== USERS ===")

    users = session.execute(
        select(User)
    ).scalars()

    for user in users:
        print(
            f"ID={user.id} | "
            f"Name={user.name} | "
            f"Email={user.email} | "
            f"Created={user.created_at}"
        )


# =========================================================
# PRINT TEAMS
# =========================================================
with SessionLocal() as session:

    print("\n=== TEAMS ===")

    teams = session.execute(
        select(Team)
    ).scalars()

    for team in teams:
        print(
            f"ID={team.id} | "
            f"Name={team.name} | "
            f"Created={team.created_at}"
        )


# =========================================================
# PRINT ENROLLMENTS
# =========================================================
with SessionLocal() as session:

    print("\n=== ENROLLMENTS ===")

    enrollments = session.execute(
        select(Enrollment)
    ).scalars()

    for enrollment in enrollments:
        print(
            f"UserID={enrollment.user_id} | "
            f"TeamID={enrollment.team_id} | "
            f"Role={enrollment.role} | "
            f"Created={enrollment.created_at}"
        )