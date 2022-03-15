from sqlalchemy.orm import Session
from database.models import User, Drive, engine, drive_passenger

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
    drive_pass = session.query(drive_passenger).filter_by(
        drive_id=drive.id,
        user_id=passenger.id
    ).first()
    drive_pass.passenger_count = num_of_passengers
    session.commit()
    print(drive_pass.id)
    print(drive_pass.passenger_count)
    return drive


def drive_delete_passenger(drive, passenger):
    print(drive.current_passengers_amount)
    if passenger in drive.passengers:
        drive_pass = session.query(drive_passenger).filter_by(drive_id=drive.id,user_id=passenger.id).first()
        print(drive_pass.id)
        print(drive_pass.passenger_count)
        drive.current_passengers_amount -= drive_pass.passenger_count
        drive.passengers.remove(passenger)
    print(drive.current_passengers_amount, "suka blya")
    session.commit()
    return drive


def get_drive_by(attrs):
    drive = session.query(Drive)
    for key, value in attrs.items():
        drive = drive.filter(key == value)
    return drive


def get_all_drive():
    return session.query(Drive).all()


if __name__ == "__main__":
    # some = ["da", "Da", "dA"]
    # print(some.index("Da"))
    # print(some[some.index("Da")])
    driver, created = get_or_create_user(12354)
    # drive = create_drive(place_from="da", place_to="da", driver_id=driver.id, max_passengers_amount=4, departure_time="123", comment="ads")
    driver = edit_drive(driver, {"name": "Name", "surname": "Surname", "phone_number": "+380992345123", "max_passengers_amount": 4})
    print(driver)
    drive = get_drive_by({Drive.place_from:"da", Drive.place_to:"da"}).first()
    drive = edit_drive(drive, {"current_passengers_amount": 0})
    print(drive)
    drive_add_passenger(drive, driver, 3)
    drive_delete_passenger(drive, driver)
    print(drive.passengers)
    someshit = session.query(drive_passenger).all()
    print(someshit)