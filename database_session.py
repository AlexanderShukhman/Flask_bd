from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# импортируем классы Book и Base из файла database_setup.py
from database_setup import Book, Base

engine = create_engine('sqlite:///books-collection.db')
# Свяжим engine с метаданными класса Base
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# Экземпляр DBSession() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
session = DBSession()

entryName = Book(title="Идиот", author="Достоевский Ф.М.")

# Чтобы сохранить наш объект ClassName, мы добавляем его в наш сессию:
session.add(entryName)

# Сохранение изменений
session.commit()