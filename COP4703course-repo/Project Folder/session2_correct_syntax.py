from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@db:5432/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)

create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);
"""

insert_users_sql = """
INSERT INTO users (username)
VALUES
    ('Alice'),
    ('Bob'),
    ('Charlie'),
    ('Diana');
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text(insert_users_sql))

print("Table created and users inserted!")



#
# Attempt to do bad things with a query
# Use SQLAlchemy notation
#

from sqlalchemy import text

user_input = "1; DROP TABLE users;"

query = text("SELECT * FROM users WHERE id = :id")

with engine.connect() as conn:
    result = conn.execute(query, {"id": user_input})
    print(result.fetchall())