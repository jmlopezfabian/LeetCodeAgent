
from sqlalchemy import Column, Integer, Text, create_engine, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"
df = pd.read_csv('data/leetcode_raw.csv')

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)

class ProblemInformation(Base):
    __tablename__ = "problems_info"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Text, nullable=False)
    acceptance_rate = Column(Float, nullable=True)
    frequency = Column(Float, nullable=True)
    url = Column(Text, nullable=True)
    accepted = Column(Integer, nullable=True)
    submissions = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    dislikes = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)



Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def prepare_row(row):
    def parse_number(value):
        """Cast values like '4.1M' or '2.5K' to integers"""
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return int(value)
        value_str = str(value).strip()
        if value_str.endswith("M"):
            return int(float(value_str[:-1]) * 1000000)
        elif value_str.endswith("K"):
            return int(float(value_str[:-1]) * 1000)
        else:
            try:
                return int(float(value_str))
            except (ValueError, TypeError):
                return None
    
    accepted = parse_number(row['accepted'])
    submissions = parse_number(row['submissions'])
    
    return {
        "title": row['title'],
        "description": row['description'],
        "difficulty": row['difficulty'],
        "acceptance_rate": row['acceptance_rate'],
        "frequency": row['frequency'],
        "url": row['url'],
        "accepted": accepted,
        "submissions": submissions,
        "likes": row['likes'],
        "dislikes": row['dislikes'],
        "rating": row['rating'],
    }

for index, row in df.iterrows():
    problem_info = ProblemInformation(**prepare_row(row))
    session.add(problem_info)
    session.commit()

print("Problem information inserted successfully")