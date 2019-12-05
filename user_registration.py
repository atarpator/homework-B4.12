import uuid
import datetime
import sys
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Введите регистрационные данные!")
    first_name = input("Ваше имя: ")
    last_name = input("Ваша фамилия: ")
    gender = input("Пол Male или Female: ")
    email = input("Адрес электронной почты: ")
    birthdate = input("Дата рождения ГГГГ-ММ-ДД: ")
    height = float(input("Ваш рост в см: "))

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user

def main():
    session = connect_db()
    mode = input("Регистрация нового пользователя\nДля регистрации нажмите - 1\nДля выхода нажмите - 2 \n")
    if mode == "1":
        user = request_data()
        session.add(user)
        session.commit()
        print("Спасибо, данные сохранены!")
    elif mode == "2":
        sys.exit()
    else:
        print("Некорректный режим:(")

if __name__ == "__main__":
    main()
