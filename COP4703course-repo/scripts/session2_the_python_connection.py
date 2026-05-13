# The Python Connection

import os
import psycopg2

# 12-Factor App Principle: Config in Environment
# If DB_HOST is not set, default to "postgres"

db_host = os.getenv("POSTGRES_HOST", "postgres")

try:
   conn = psycopg2.connect(
    # Container name
    host=os.getenv("POSTGRES_HOST", "psql_db"),
    # Database name
    dbname=os.getenv("POSTGRES_DB", "my_db"),
    user=os.getenv("POSTGRES_USER", "admin"),
    password=os.getenv("POSTGRES_PASSWORD", "password")
)

   print(f"Connected to {db_host} successfully!")

except Exception as e:
   print(f"Connection failed: {e}")