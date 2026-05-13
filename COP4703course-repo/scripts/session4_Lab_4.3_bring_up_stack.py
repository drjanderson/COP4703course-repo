from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# -----------------------------------
# DATABASE CONNECTION
# Use Docker service name: psql_db
# -----------------------------------
engine = create_engine(
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db",
    echo=True
)

# -----------------------------------
# BASE CLASS
# -----------------------------------
class Base(DeclarativeBase):
    pass

# -----------------------------------
# USER MODEL
# Note: user_emails has a foreign key constraint.
# -----------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)


class UserEmail(Base):
    __tablename__ = "user_emails"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email = Column(String)
# -----------------------------------
# DROP and CREATE TABLES
# -----------------------------------
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# -----------------------------------
# SESSION FACTORY
# -----------------------------------
SessionLocal = sessionmaker(bind=engine)

# -----------------------------------
# INSERT USER
# -----------------------------------
with SessionLocal() as session:

    new_user = User(
        name="Alice",
        email="alice@example.com"
    )

    session.add(new_user)

    # Save changes to DB
    session.commit()

# -----------------------------------
# QUERY USER BACK
# -----------------------------------
with SessionLocal() as session:

    stmt = select(User).where(User.name == "Alice")

    result = session.execute(stmt)

    user = result.scalar_one()

    print("\n=== USER FOUND ===")
    print(f"ID: {user.id}")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")