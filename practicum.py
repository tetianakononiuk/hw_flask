# 1. Разработайте модель Transaction для управления финансовыми операциями.
# Модель должна содержать:
# ● amount (десятичное число),
# ● transaction_type (строка, принимает значения "debit" или "credit"),
# ● currency (строка).


from pydantic import BaseModel, constr, condecimal


class Transaction(BaseModel):
    amount: condecimal(gt=0)
    transaction_type: constr(pattern="^(debit|credit)$")
    currency: constr(min_length=3, max_length=3)

    class Config:
       strip_whitespace = True


transaction = Transaction(amount=150.50, transaction_type="debit", currency="USD")
print(transaction)


# 2. Создайте модель Appointment для записи на прием, которая включает patient_name (строка),
# appointment_date (дата и время), и проверку, что запись не может быть установлена ранее, чем
# через 24 часа от текущего момента.


from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator, Field


class Appointment(BaseModel):
    patient_name: str
    appointment_date: datetime

    @field_validator('appointment_date')
    def check_date(cls, value):
        if value < datetime.now() +timedelta(days=1):
            raise ValueError("Error Validator")
        return  value


appointment = Appointment(patient_name="Alice", appointment_date=datetime.now()+timedelta(hours=26))
print(appointment)

# 3. Напишите код для создания движка SQLAlchemy с подключением к базе данных SQLite,
# который будет располагаться в памяти, и настройте вывод логов всех операций с базой
# данных на экран.


from sqlalchemy import create_engine
import logging
logging.basicConfig(level=logging.INFO)
engine = create_engine('sqlite:///:memory:', echo=True)

# 4. Создайте модель User с полями:
#  id (целочисленный тип, первичный ключ),
#  name (строковый тип, длина до 50 символов),
#  age (целочисленный тип).

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

# 5. Определите две модели, User и Post, где пользователь может иметь много постов (один
# ко многим). Используйте декларативный базовый класс.

from sqlalchemy import Column, Integer, String, ForeignKey
from  sqlalchemy.orm import relationship, declarative_base
from SQLAlchemy.__init__ import engine


Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")


Base.metadata.create_all(engine)


# 6. Используя ранее определённые модели User и Address, создайте нового пользователя и
# адрес, добавьте их в базу данных с помощью сессии, затем удалите пользователя и
# проверьте изменения.


from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="John Doe", age=30)
new_post = Post(user=new_user, title="John's First Post")

session.add(new_user)
session.add(new_post)
session.commit()

print(f'Added User:{session.query(User).all()}')
print(f'Added Post:{session.query(Post).all()}')

session.delete(new_user)
session.commit()

print(f'Remaining Users: {session.query(User).all()}')
print(f'Remaining Posts: {session.query(Post).all()}')

session.close()

# 7. Найдите и исправьте ошибки в следующем коде

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


engine = create_engine('sqlite:///example.db')

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('persons.id'))
    owner = relationship("Person", back_populates="pets")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_person = Person(name='Alice')
new_pet = Pet(name='Fido', owner=new_person)
session.add(new_person)
session.add(new_pet)
session.commit()
session.close()
