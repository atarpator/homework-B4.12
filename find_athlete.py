import datetime

import sqlalchemy as sa
from sqlalchemy import Column as Col
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete'
    id = Col(sa.Integer, primary_key=True)
    age = Col(sa.Integer)
    birthdate = Col(sa.Text)
    gender = Col(sa.Text)
    height = Col(sa.Float)
    weight = Col(sa.Integer)
    name = Col(sa.Text)
    gold_medals = Col(sa.Integer)
    silver_medals = Col(sa.Integer)
    bronze_medals = Col(sa.Integer)
    total_medals = Col(sa.Integer)
    sport = Col(sa.Text)
    country = Col(sa.Text)

class User(Base):
    __tablename__ = 'user'
    id = Col(sa.String(36), primary_key=True)
    first_name = Col(sa.Text)
    last_name = Col(sa.Text)
    gender = Col(sa.Text)
    email = Col(sa.Text)
    birthdate = Col(sa.Text)
    height = Col(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("\nНайти атлета, параметры которого близки к пользователю")
    user_id = input("\nВведите id пользователя: ")
    return int(user_id)

def change_string_to_date(date_string):
    date_split = date_string.split("-")
    date_int = [int(x) for x in date_split]
    date = datetime.date(*date_int)
    return date

def search_date(user, session):
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = change_string_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = change_string_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd

    return athlete_id, athlete_bd


def search_height(user, session):
    athletes_list = session.query(Athelete).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height

def main():
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя не существует:(")
    else:
        bd_athlete, bd = search_date(user, session)
        height_athlete, height = search_height(user, session)
        print(
            "\nID атлета, наиболее близкого по дате рождения: {}\nДень рождения атлета: {}\n".format(bd_athlete, bd)
        )
        print(
            "ID атлета, наиболее близкого по росту: {}\nРост атлета: {}\n".format(height_athlete, height)
        )

if __name__ == "__main__":
    main()
