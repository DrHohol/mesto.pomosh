import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, String, Boolean, ForeignKey
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship
from sqlalchemy.ext.associationproxy import association_proxy


load_dotenv()
engine = create_engine("postgresql+psycopg2:" + os.environ.get("DATABASE_URL"))
engine.connect()

session = sessionmaker()
session.configure(bind=engine)
session = Session(bind=engine)
Base = declarative_base()


class DrivePassenger(Base):
    __tablename__ = "drive_passenger"

    drive_id = Column(ForeignKey("drive.id"), primary_key=True)
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    drive = relationship("Drive", backref="drive_associations")
    user = relationship("User", backref="user_associations")
    passenger_count = Column(Integer)


class Drive(Base):
    __tablename__ = "drive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    place_from = Column(String(255))
    place_to = Column(String(255))
    passengers = relationship('User', secondary="drive_passenger")
    driver_id = Column(Integer, ForeignKey("user.id"))
    driver = relationship("User", backref="drive_driver")
    max_passengers_amount = Column(Integer, default=4)
    current_passengers_amount = Column(Integer, default=0)
    departure_time = Column(String(255))
    is_done = Column(Boolean, default=False)
    comment = Column(Text)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    place_from = Column(String(255), nullable=True)
    place_to = Column(String(255), nullable=True)
    active_search = Column(Boolean, default=False)
    num_of_passengers = Column(Integer, default=1)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
