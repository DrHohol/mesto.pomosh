import datetime

from sqlalchemy.orm import Session
from database.models import User, Drive, engine

session = Session(engine)


def get_or_create_user(chat_id):
    user = session.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        user = User(chat_id=chat_id)
        session.add(user)
        session.commit()
        return user, True
    return user, False


def edit_user(user, attrs):
    for key, value in attrs.items():
        setattr(user, key, value)
    session.commit()
    return user


def create_drive(place_from, place_to, driver_id, max_passengers_amount, departure_time, comment=None):
    driver, created = get_or_create_user(driver_id)
    if created:
        session.commit()
    drive = Drive(
        place_from=place_from,
        place_to=place_to,
        driver_id=driver.id,
        max_passengers_amount=max_passengers_amount,
        departure_time=departure_time,
    )
    if comment:
        drive.comment = comment
    session.add(drive)
    session.commit()
    return drive


def edit_drive(drive_id, attrs):
    drive = session.query(Drive).filter(Drive.id == drive_id).first()
    for key, value in attrs.items():
        setattr(drive, key, value)
    session.commit()
    return drive


def get_drive_by(attrs, places=0):
    drive = session.query(Drive)
    for key, value in attrs.items():
        if key == Drive.place_to and value == "any":
            continue
        drive = drive.filter(key == value)
    drive = drive.filter(Drive.max_passengers_amount >= places).all()
    return drive


def get_user_by(place_from, place_to=None, num_of_passenger=None):
    users = session.query(User).filter(User.place_from == place_from,
                                       User.active_search == True)
    if place_to:
        users = users.filter(User.place_to == place_to)
    if num_of_passenger:
        users = users.filter(User.num_of_passengers <= num_of_passenger)
    return users.all()


def delete_drive(drive):
    session.delete(drive)
    session.commit()


def get_all_drive():
    return session.query(Drive).all()


if __name__ == "__main__":
    driver, created = get_or_create_user(1235)
