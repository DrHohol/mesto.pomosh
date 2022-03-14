from sqlalchemy.orm import Session
from database.models import User, Drive, engine

session = Session(engine)


def get_or_create_user(chat_id, name, surname, phone_number):
    user = session.query(User).filter(User.chat_id==chat_id).first()
    if not user:
        user = User(chat_id=chat_id)
    user.name = name
    user.surname = surname
    user.phone_number = phone_number
    session.add(user)
    session.commit()
    return user

def get_or_create_drive():

    pass