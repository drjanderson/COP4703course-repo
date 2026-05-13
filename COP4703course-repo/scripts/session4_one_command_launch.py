from sqlalchemy import create_engine, text

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
engine = create_engine(
    "postgresql+psycopg2://admin:mysecretpassword@psql_db:5432/my_db",
    echo=True
)

# -----------------------------------
# CREATE TABLES + INSERT DATA
# -----------------------------------
with engine.begin() as conn:

    # Drop tables if they already exist
    conn.execute(text("""
        DROP TABLE IF EXISTS user_emails;
    """))

    conn.execute(text("""
        DROP TABLE IF EXISTS users;
    """))

    # -----------------------------------
    # CREATE USERS TABLE
    # -----------------------------------
    conn.execute(text("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL
        );
    """))

    # -----------------------------------
    # CREATE USER EMAILS TABLE
    # -----------------------------------
    conn.execute(text("""
        CREATE TABLE user_emails (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            email TEXT NOT NULL
        );
    """))

    # -----------------------------------
    # INSERT USERS
    # -----------------------------------
    conn.execute(text("""
        INSERT INTO users (username)
        VALUES
            ('alice'),
            ('bob'),
            ('charlie');
    """))

    # -----------------------------------
    # INSERT EMAILS
    # -----------------------------------
    conn.execute(text("""
        INSERT INTO user_emails (user_id, email)
        VALUES
            (1, 'alice@example.com'),
            (2, 'bob@example.com'),
            (3, 'charlie@example.com');
    """))

print("\nTables created and populated successfully.\n")

# -----------------------------------
# DISPLAY DATA
# -----------------------------------
with engine.connect() as conn:

    result = conn.execute(text("""
        SELECT
            users.id,
            users.username,
            user_emails.email
        FROM users
        JOIN user_emails
            ON users.id = user_emails.user_id
        ORDER BY users.id;
    """))

    print("=== USER DIRECTORY ===")

    for row in result:
        print(f"ID: {row.id} | User: {row.username} | Email: {row.email}")