import os
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, DateTime, Boolean, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime


# URL для подключения к базе данных PostgreSQL
from app.api.identification import DATABASE_URL
url = DATABASE_URL

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание базовой модели
Base = declarative_base()


# Модель для таблицы bestiariesList
class Bestiaries(Base):
    __tablename__ = 'bestiaries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # TODO добавить ForeignKey('users.id')
    author = Column(Integer)
    date_creation = Column(DateTime, default=datetime.utcnow)
    latest_update = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    is_star = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    average_rating = Column(Float, default=0.0)
    rang = Column(Float, default=0.0)
    count_views = Column(Integer, default=0)
    src_icon = Column(String, default='/download/default-bestiary-icon.png')
    src_background_img = Column(String, default='')
    description = Column(String, default='')

    categories = relationship("Category", back_populates="bestiaries")
    entities = relationship("Entity", back_populates="bestiaries")


# Модель для таблицы categories
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    bestiaries_id = Column(Integer, ForeignKey('bestiaries.id'))
    name = Column(String)
    background_img = Column(String)
    background_color = Column(String)

    bestiaries = relationship("Bestiaries", back_populates="categories")
    entities = relationship("Entity", back_populates="category")


# Модель для таблицы entities
class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, index=True)
    bestiaries_id = Column(Integer, ForeignKey('bestiaries.id'))
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    img_name = Column(String)
    background_color = Column(String)

    bestiaries = relationship("Bestiaries", back_populates="entities")
    category = relationship("Category", back_populates="entities")


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Пример использования
if __name__ == "__main__":
    db = SessionLocal()

    # Пример создания нового бестиария
    new_bestiary = Bestiaries(name="My Bestiary", author=0, average_rating=4.5, count_views=30)
    db.add(new_bestiary)
    db.commit()

    # Пример создания новой категории
    new_category = Category(bestiaries_id=new_bestiary.id, name="Monsters", background_img="monsters.jpg",
                            background_color="#FF0000")
    db.add(new_category)
    db.commit()

    # Пример создания новой сущности
    new_entity = Entity(bestiaries_id=new_bestiary.id, name="Dragon", description="A fire-breathing creature",
                        category_id=new_category.id, img_name="dragon.jpg", background_color="#00FF00")
    db.add(new_entity)
    db.commit()

    db.close()
