from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy_serializer import SerializerMixin

# создание экземпляра declarative_base
Base = declarative_base()

# мы создаем класс Book наследуя его из класса Base.
class Book(Base, SerializerMixin):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))


# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///books-collection.db')

Base.metadata.create_all(engine)