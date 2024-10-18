from fastapi import FastAPI, HTTPException
from app.api.db import SessionLocal, Bestiaries, Category, Entity
from sqlalchemy import and_, or_

from app.api.models import *   # Модели Pydantic для валидации данных


app_debug = FastAPI(
    title="debug API",
    description='''\tRU:
\t\tВременная API исключительно для тестов и простого заполнения БД разными данными. Перед окончательным запуском приложения - удалить эту API

\t\tУдаление настоящее без возможности восстановить записи!
___

\tEN:
\t\tFUCK YOU
    ''',
    version="0.0.1",
)


# Создание нового бестиария
@app_debug.post("/bestiaries/", response_model=BestiariesOut, tags=["bestiaries"])
def create_bestiary(bestiary: BestiariesCreate):
    db = SessionLocal()
    db_bestiary = Bestiaries(**bestiary.dict())
    db.add(db_bestiary)
    db.commit()
    db.refresh(db_bestiary)
    db.close()
    return db_bestiary


# Получение списка всех бестиариев
@app_debug.get("/bestiaries/", response_model=List[BestiariesOut], tags=["bestiaries"])
def read_bestiaries():
    db = SessionLocal()
    bestiaries = db.query(Bestiaries).all()
    db.close()
    return bestiaries


# Удаление бестиария по ID
@app_debug.delete("/bestiaries/{bestiary_id}", response_model=BestiariesOut, tags=["bestiaries"])
def delete_bestiary(bestiary_id: int):
    db = SessionLocal()
    bestiary = db.query(Bestiaries).filter(Bestiaries.id == bestiary_id).first()
    if bestiary is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    db.delete(bestiary)
    db.commit()
    db.close()
    return bestiary


# Удаление ВСЕХ бестиариев
@app_debug.delete("/bestiaries", response_model=str, tags=["bestiaries"])
def delete_all_bestiary():
    db = SessionLocal()
    bestiaries = db.query(Bestiaries).all()
    for bestiary in bestiaries:
        db.delete(bestiary)
    db.commit()
    db.close()
    return 'all bestiaries have been successfully deleted'


# ___________________________ categories ________________________________


# Создание новой категории
@app_debug.post("/categories/", response_model=CategoryOut, tags=["categories"])
def create_category(category: CategoryCreate):
    db = SessionLocal()
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category


# Получение списка всех категорий
@app_debug.get("/categories/", response_model=List[CategoryOut], tags=["categories"])
def read_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    db.close()
    return categories


# Удаление категории по ID
@app_debug.delete("/categories/{category_id}", response_model=CategoryOut, tags=["categories"])
def delete_category(category_id: int):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    db.delete(category)
    db.commit()
    db.close()
    return category


# Удаление ВСЕХ категорий
@app_debug.delete("/categories/", response_model=str, tags=["categories"])
def delete_all_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    for category in categories:
        db.delete(category)
    db.commit()
    db.close()
    return 'all categories have been successfully deleted'


# ___________________________ entities ________________________________


# Создание новой сущности
@app_debug.post("/entities/", response_model=EntityOut, tags=["entities"])
def create_entity(entity: EntityCreate):
    db = SessionLocal()
    db_entity = Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    db.close()
    return db_entity


# Получение списка всех сущностей
@app_debug.get("/entities/", response_model=List[EntityOut], tags=["entities"])
def read_entities():
    db = SessionLocal()
    entities = db.query(Entity).all()
    db.close()
    return entities


# Получение сущности по ID
@app_debug.get("/entities/{entity_id}", response_model=EntityOut, tags=["entities"])
def read_entity(entity_id: int):
    db = SessionLocal()
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    db.close()
    if entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


# Удаление сущности по ID
@app_debug.delete("/entities/{entity_id}", response_model=EntityOut, tags=["entities"])
def delete_entity(entity_id: int):
    db = SessionLocal()
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if entity is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    db.delete(entity)
    db.commit()
    db.close()
    return entity


# Удаление ВСЕХ сущностей
@app_debug.delete("/entities", response_model=str, tags=["entities"])
def delete_all_entities():
    db = SessionLocal()
    entities = db.query(Entity).all()
    for entity in entities:
        db.delete(entity)
    db.commit()
    db.close()
    return 'all entities have been successfully deleted'
