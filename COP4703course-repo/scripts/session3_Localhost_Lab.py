from sqlalchemy import create_engine, text

# The string you just built
DATABASE_URL = "postgresql+psycopg2://admin:mysecretpassword@localhost:5432/postgres"

# DATABASE_URL = "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/postgres"


# The Engine: The starting point for any SQLAlchemy application
engine = create_engine(DATABASE_URL)

# The connection actually opens here (Lazy Initialization)
with engine.connect() as conn:  # The bridge opens here
   result = conn.execute(text("SELECT 1"))
   print("Connection Successful!") # bridge closes automatically
