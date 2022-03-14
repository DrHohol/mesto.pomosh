import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship

load_dotenv()
engine = create_engine("postgresql+psycopg2:" + os.environ.get("DATABASE_URL"))
engine.connect()

session = sessionmaker()
session.configure(bind=engine)
session = Session(bind=engine)
Base = declarative_base()

drive_passenger = Table(
    "drive_passenger",
    Base.metadata,
    Column("drive_id", Integer, ForeignKey("drive.id")),
    Column("passenger_id", Integer, ForeignKey("passenger.id"))
)


class Drive(Base):
    __tablename__ = "drive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    place_from = Column(String(255))
    place_to = Column(String(255))
    driver = Column(Integer, ForeignKey("driver.id"))
    driver_id = relationship("Driver", backref="drive")
    max_passengers_amount = Column(Integer)
    passengers = relationship('Passenger', secondary=drive_passenger, backref='drive')
    departure_time = Column(String(255))
    is_done = Column(Boolean, default=False)
    comment = Column(Text)


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, autoincrement=True, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)


class Passenger(Base):
    __tablename__ = "passenger"

    id = Column(Integer, autoincrement=True, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    place_from = Column(String(255))
    place_to = Column(String(255), nullable=True)


Base.metadata.create_all(engine)