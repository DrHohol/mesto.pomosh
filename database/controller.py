from sqlalchemy.orm import Session
from database.models import User, Drive, engine

session = Session(engine)


def get_or_create_user(chat_id, name, surname, phone_number):
    user = session.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        user = User(chat_id=chat_id)
    user.name = name
    user.surname = surname
    user.phone_number = phone_number
    session.add(user)
    session.commit()
    return user


def edit_user(user, name=None, surname=None, phone_number=None, place_from=None, place_to=None, active_search=None):
    if name:
        user.name = name
    if surname:
        user.surname = surname
    if phone_number:
        user.phone_number = phone_number
    if place_from:
        user.place_from = place_from
    if place_to:
        user.place_to = place_to
    if active_search is not None:
        user.active_search = active_search
    session.commit()
    return user


def create_drive(place_from, place_to, driver_id, max_passengers_amount, departure_time, comment):
    drive = Drive(
        place_from=place_from,
        place_to=place_to,
        driver_id=driver_id,
        max_passengers_amount=max_passengers_amount,
        departure_time=departure_time,
        comment=comment
        )
    session.add(drive)
    session.commit()
    return drive


def edit_drive(drive,
               place_from=None,
               place_to=None,
               max_passengers_amount=None,
               departure_time=None,
               comment=None,
               is_done=None):
    if place_from:
        drive.place_from = place_from
    if place_to:
        drive.place_to = place_to
    if max_passengers_amount:
        drive.max_passengers_amount = max_passengers_amount
    if departure_time:
        drive.departure_time = departure_time
    if is_done is not None:
        drive.is_done = is_done
    if comment:
        drive.comment = comment
    session.commit()
    return drive


def drive_add_passenger(drive, passenger):
    if passenger not in drive.passengers and drive.max_passengers_amount < len(drive.passengers):
        drive.passengers.append(passenger)
    session.commit()
    return drive


def drive_delete_passenger(drive, passenger):
    if passenger in drive.passengers:
        drive.passengers.remove(passenger)
    session.commit()
    return drive


def get_drive_by():
    pass
