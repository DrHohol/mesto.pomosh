import asyncio
import datetime
import os

import pytz
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, subqueryload
from database.models import User, Drive

db_link = os.environ.get("DATABASE_URL_ASYNC")
async_engine = create_async_engine(db_link, pool_size=30, pool_timeout=300)
async_session = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_or_create_user(chat_id):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User).filter(User.chat_id == chat_id)
            )
            user = user.scalars().first()
            created = False
            if not user:
                user = User(chat_id=chat_id)
                session.add(user)
                await session.commit()
                created = True
            session.expunge(user)
            return user, created


async def edit_user(user, attrs):
    async with async_session() as session:
        async with session.begin():
            session.add(user)
            for key, value in attrs.items():
                setattr(user, key, value)
            await session.commit()
            session.expunge(user)
            return user


async def create_drive(place_from, place_to, driver_id, max_passengers_amount, departure_time=None, comment=None,regular=False):
    driver, created = await get_or_create_user(driver_id)
    async with async_session() as session:
        async with session.begin():
            session.add(driver)
            drive = Drive(
                place_from=place_from,
                place_to=place_to,
                driver_id=driver.id,
                max_passengers_amount=max_passengers_amount,
                departure_time=departure_time,
                regular=regular
            )
            if comment:
                drive.comment = comment
            session.add(drive)
            await session.commit()
            drive = await session.execute(
                select(Drive).options(subqueryload(Drive.driver)).filter(Drive.id == drive.id)
            )
            return drive


async def edit_drive(drive_id, attrs):
    async with async_session() as session:
        async with session.begin():
            drive = await session.execute(
                select(Drive).filter(Drive.id == drive_id)
            )
            drive = drive.scalars().first()
            for key, value in attrs.items():
                setattr(drive, key, value)
            await session.commit()
            session.expunge(drive)
            return drive


async def get_drive_by(attrs, places=0):
    async with async_session() as session:
        async with session.begin():
            drive = select(Drive).options(subqueryload(Drive.driver))
            for key, value in attrs.items():
                if key == Drive.place_to and value == "Неважливо":
                    continue
                drive = drive.filter(key == value)
            drive = drive.filter(Drive.max_passengers_amount >= places)
            drive = await session.execute(
                drive
            )
            drive = drive.scalars().all()
            return drive


async def get_user_by(place_from, place_to=None, num_of_passenger=None):
    async with async_session() as session:
        async with session.begin():
            users = select(User).filter(User.place_from == place_from,
                                       User.active_search == True)
            if place_to:
                users = users.filter(User.place_to == place_to)
            if num_of_passenger:
                users = users.filter(User.num_of_passengers <= num_of_passenger)
            users = await session.execute(
                users
            )
            return users.scalars().all()


async def delete_drive(drive):
    async with async_session() as session:
        async with session.begin():
            session.add(drive)
            await session.delete(drive)
            await session.commit()


async def get_all_drive():
    async with async_session() as session:
        async with session.begin():
            drives = await session.execute(
                select(Drive)
            )
            drives = drives.scalars().all()
            session.expunge_all()
            return drives

async def get_all_users():
    async with async_session() as session:
        async with session.begin():
            users = await session.execute(
                select(User)
            )
            users = users.scalars().all()
            return users


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    driver, created = loop.run_until_complete(get_or_create_user(1235))
    print(driver, created)
    print(driver.registration_time)