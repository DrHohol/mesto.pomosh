import datetime

from sqlalchemy.orm import Session
from database.models import User, Drive, engine, DrivePassenger

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


def edit_drive(drive, attrs):
    for key, value in attrs.items():
        setattr(drive, key, value)
    session.commit()
    return drive


def drive_add_passenger(drive, passenger, num_of_passengers=1):
    if passenger not in drive.passengers and drive.max_passengers_amount > drive.current_passengers_amount:
        drive.passengers.append(passenger)
        drive.current_passengers_amount += num_of_passengers
        session.commit()
        drive_pass = session.query(DrivePassenger).filter_by(
            drive_id=drive.id,
            user_id=passenger.id
        ).first()
        drive_pass.passenger_count = num_of_passengers
        session.commit()
    return drive


def drive_delete_passenger(drive, passenger):
    print(drive.current_passengers_amount)
    if passenger in drive.passengers:
        drive_pass = session.query(DrivePassenger).filter_by(drive_id=drive.id,user_id=passenger.id).first()
        drive.current_passengers_amount -= drive_pass.passenger_count
        drive.passengers.remove(passenger)
    print(drive.current_passengers_amount)
    session.commit()
    return drive


def get_drive_by(attrs, places=0):
    drive = session.query(Drive)
    for key, value in attrs.items():
        if key == Drive.place_to and value == "any":
            continue
        drive = drive.filter(key == value)
    drive = drive.filter(Drive.max_passengers_amount-Drive.current_passengers_amount >= places, Drive.is_done == False).all()
    return drive


def get_user_by(place_from, place_to=None, num_of_passenger=1):
    users = session.query(User).filter_by(User.place_from == place_from)
    if place_to:
        users = users.filter(User.place_to == place_to)
    if num_of_passenger:
        users = users.filter(User.num_of_passengers == num_of_passenger)
    return users.all()


def delete_drive(drive):
    session.delete(drive)
    session.commit()


def get_all_drive():
    return session.query(Drive).all()


if __name__ == "__main__":
    driver, created = get_or_create_user(12354)
    drive = create_drive(place_from="da", place_to="da", driver_id=driver.id, max_passengers_amount=4, departure_time=datetime.datetime.now(), comment="ads")
    driver = edit_user(driver, {"name": "Name", "surname": "Surname", "phone_number": "+380992345123", "max_passengers_amount": 4})
    drive = get_drive_by({Drive.place_from:"da", Drive.place_to:"da"})
    print(drive)
    drive = edit_drive(drive[0], {"current_passengers_amount": 0})
    drive_add_passenger(drive, driver, 3)
    drive_delete_passenger(drive, driver)
    drive = get_drive_by(attrs={}, places=2)
    print(session.query(User).first().drive)
