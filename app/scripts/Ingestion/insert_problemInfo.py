
from dataclasses import FrozenInstanceError
from sqlalchemy import Column, Integer, Text, create_engine, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"
print(DATABASE_URL)
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

for index, row in df.iterrows():
    problem_info = ProblemInformation(
        title=row['title'],
        description=row['description'],
        difficulty=row['difficulty'],
        acceptance_rate=row['acceptance_rate'],
        frequency=row['frequency'],
        url=row['url'],
        accepted=row['accepted'],
        submissions=row['submissions'],
        likes=row['likes'],
        dislikes=row['dislikes'],
        rating=row['rating'],
    )
    session.add(problem_info)
    session.commit()

print("Problem information inserted successfully")