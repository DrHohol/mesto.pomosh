import datetime
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship

load_dotenv()
engine = create_engine(os.environ.get("DATABASE_URL"))
engine.connect()

session = sessionmaker()
session.configure(bind=engine)
session = Session(bind=engine)
Base = declarative_base()


class Drive(Base):
    __tablename__ = "drive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    place_from = Column(String(255))
    place_to = Column(String(255))
    driver_id = Column(Integer, ForeignKey("user.id"))
    driver = relationship("User", backref="drive_driver")
    max_passengers_amount = Column(Integer, default=4)
    departure_time = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)
    regular = Column(Boolean, default=False)
    creation_time = Column(DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(hours=3))

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    name = Column(String(255), nullable=True)
    contact_info = Column(String(255), nullable=True)
    place_from = Column(String(255), nullable=True)
    place_to = Column(String(255), nullable=True)
    active_search = Column(Boolean, default=False)
    num_of_passengers = Column(Integer, default=1)
    registration_time = Column(DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(hours=3), nullable=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
