import os
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the Model
class CalendarData(Base):
    __tablename__ = "calendar_data"
    id = Column(Integer, primary_key=True)
    month_name = Column(String, nullable=False)
    day_number = Column(Integer, nullable=False)

# Create the table
Base.metadata.create_all(engine)

# Data for seeding
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

print("Seeding 50,000 rows...")

# Bulk insert for efficiency
batch_size = 5000
for i in range(0, 50000, batch_size):
    batch = []
    for _ in range(batch_size):
        month = random.choice(months)
        day = random.randint(1, 28) # Keep it simple for the demo
        batch.append(CalendarData(month_name=month, day_number=day))
    
    session.bulk_save_objects(batch)
    session.commit()
    print(f"Inserted {i + batch_size} rows...")

print("Seeding complete.")