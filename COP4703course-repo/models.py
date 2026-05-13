from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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
