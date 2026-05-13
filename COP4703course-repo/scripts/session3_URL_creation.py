import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text

# Best practice: Use the URL object contstructor
# This handles encoding automatically

connection_URL = URL.create(
    drivername = "postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"), # "psql_db" in docker-compose
    port=5432,
    database=os.getenv("POSTGRES_DB")
)

engine = create_engine(connection_URL)

# The connection actually opens here (Lazy Initialization)
with engine.connect() as conn:  # The bridge opens here
   result = conn.execute(text("SELECT 1"))
   print("Connection Successful!") # bridge closes automatically
