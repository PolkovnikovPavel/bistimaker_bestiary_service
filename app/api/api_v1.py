from fastapi import FastAPI, HTTPException
from app.api.db import SessionLocal, Bestiaries, Category, Entity
from sqlalchemy import and_, or_

from app.api.models import *   # Модели Pydantic для валидации данных
from app.api.including_redis import *


app_v1 = FastAPI(
    title="bestiary API",
    description='''\tRU:
\t\tAPI предоставляет инструменты по стандарту CRUD для редактирования бестиариев, категорий существ и самих существ. Все изменения сохраняются в базе данных.

\t\tУдаление бестиариев не стирает данные насовсем, но восстановить их с помощью API невозможно.
___

\tEN:
\t\tThe API provides tools according to the CRUD standard for editing bestiaries, categories of entities and an entities. All changes are saved in the database.

\t\tDeleting bestiaries does not erase the data at all, but it is impossible to restore them using this API.
    ''',
    version="1.2.0",
)


# Создание нового бестиария
@app_v1.post("/bestiaries/", response_model=BestiariesOut, tags=["bestiaries"])
def create_bestiary(bestiary: BestiariesCreate):
    db = SessionLocal()
    db_bestiary = Bestiaries(**bestiary.dict())
    db.add(db_bestiary)
    db.commit()
    db.refresh(db_bestiary)
    db.close()

    delete_cache_from_redis('all_bestiaries', str(bestiary.author))
    return db_bestiary


# Получение списка всех бестиариев для пользователя
@app_v1.get("/bestiaries/", response_model=List[BestiariesOut], tags=["bestiaries"])
def read_bestiaries(bestiary: BestiariesGetIn):
    # TODO удалить этот вывод ключей
    all_keys = redis_client.keys('*')
    for key in all_keys:
        print(key.decode('utf-8'))

    cached_data = get_cache_from_redis('all_bestiaries', str(bestiary.author))
    if cached_data:
        return cached_data
    db = SessionLocal()
    bestiaries = db.query(Bestiaries).filter(and_(Bestiaries.author == bestiary.author,
                                                  Bestiaries.is_deleted == False)
                                             ).all()
    db.close()

    set_cache('all_bestiaries', str(bestiary.author), bestiaries)
    return bestiaries


# Получение бестиария по ID
@app_v1.get("/bestiaries/{bestiary_id}", response_model=BestiariesOut, tags=["bestiaries"])
def read_bestiary(bestiary_id: int, bestiary: BestiariesGetIn):
    cached_data = get_cache_from_redis(f'bestiary_{bestiary.author}', str(bestiary_id))
    if cached_data:
        return cached_data
    db = SessionLocal()
    db_bestiary = db.query(Bestiaries).filter(and_(Bestiaries.id == bestiary_id,
                                                   Bestiaries.author == bestiary.author,
                                                   Bestiaries.is_deleted == False)
                                              ).first()
    db.close()
    if db_bestiary is None:
        raise HTTPException(status_code=404, detail="Bestiary not found")

    set_cache(f'bestiary_{bestiary.author}', str(bestiary_id), db_bestiary)
    return db_bestiary


# Удаление бестиария по ID
@app_v1.delete("/bestiaries/{bestiary_id}", response_model=BestiariesCreate, tags=["bestiaries"])
def delete_bestiary(bestiary_id: int, bestiary: BestiariesGetIn):
    db = SessionLocal()
    db_bestiary = db.query(Bestiaries).filter(and_(Bestiaries.id == bestiary_id,
                                                   Bestiaries.author == bestiary.author)
                                              ).first()
    if db_bestiary is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    db_bestiary.is_deleted = True
    db.commit()
    db.close()

    delete_cache_from_redis('all_bestiaries', str(bestiary.author))
    delete_cache_from_redis(f'bestiary_{bestiary.author}', str(bestiary_id))
    return db_bestiary


# Изменение бестиария по ID
@app_v1.put("/bestiaries/{bestiary_id}", response_model=BestiariesOut, tags=["bestiaries"])
def update_bestiary(bestiary_id: int, bestiary: BestiariesUpdate):
    db = SessionLocal()
    db_bestiary = db.query(Bestiaries).filter(and_(Bestiaries.id == bestiary_id,
                                                   Bestiaries.author == bestiary.author)
                                              ).first()
    if db_bestiary is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    for key, value in bestiary.dict().items():
        if key == 'author' or key == 'average_rating' or key == 'count_views':
            continue
        if value is not None and hasattr(Bestiaries, key):
            setattr(db_bestiary, key, value)

    db.commit()
    db.refresh(db_bestiary)
    db.close()

    delete_cache_from_redis('all_bestiaries', str(bestiary.author))
    delete_cache_from_redis(f'bestiary_{bestiary.author}', str(bestiary_id))
    return db_bestiary


# ___________________________ categories ________________________________


# Создание новой категории
@app_v1.post("/categories/", response_model=CategoryOut, tags=["categories"])
def create_category(category: CategoryCreate):
    db = SessionLocal()
    category_dict = {k: v for k, v in category.dict().items() if k != "author"}
    db_category = Category(**category_dict)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()

    delete_cache_from_redis(f'all_categories_{category.bestiaries_id}', str(category.author))
    return db_category


# Получение списка всех категорий
@app_v1.get("/categories/", response_model=List[CategoryOut], tags=["categories"])
def read_categories(category: CategoryGetIn):
    cached_data = get_cache_from_redis('all_categories', str(category.author))
    if cached_data:
        return cached_data
    db = SessionLocal()
    bestiary = db.query(Bestiaries).filter(and_(Bestiaries.id == category.bestiaries_id,
                                                Bestiaries.author == category.author,
                                                Bestiaries.is_deleted == False)
                                           ).first()
    if bestiary is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    categories = db.query(Category).filter(Category.bestiaries_id == category.bestiaries_id).all()
    db.close()

    set_cache(f'all_categories_{category.bestiaries_id}', str(category.author), categories)
    return categories


# Получение категории по ID
@app_v1.get("/categories/{category_id}", response_model=CategoryOut, tags=["categories"])
def read_category(category_id: int, category: CategoryGetIn):
    cached_data = get_cache_from_redis(f'category_{category.author}', str(category_id))
    if cached_data:
        return cached_data
    db = SessionLocal()
    db_category = db.query(Category).filter(and_(Category.id == category_id,
                                                 Category.bestiaries_id == category.bestiaries_id)
                                            ).first()
    db.close()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    set_cache(f'category_{category.author}', str(category_id), db_category)
    return db_category


# Удаление категории по ID
@app_v1.delete("/categories/{category_id}", response_model=CategoryOut, tags=["categories"])
def delete_category(category_id: int, category: CategoryGetIn):
    db = SessionLocal()
    db_category = db.query(Category).filter(and_(Category.id == category_id,
                                                 Category.bestiaries_id == category.bestiaries_id)
                                            ).first()
    if db_category is None:
        db.close()
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    db.close()

    delete_cache_from_redis(f'all_categories_{category.bestiaries_id}', str(category.author))
    delete_cache_from_redis(f'category_{category.author}', str(category_id))
    return db_category


# Изменение категории по ID
@app_v1.put("/categories/{category_id}", response_model=CategoryOut, tags=["categories"])
def update_category(category_id: int, category: CategoryUpdate):
    db = SessionLocal()
    db_category = db.query(Category).filter(and_(Category.id == category_id,
                                                 Category.bestiaries_id == category.bestiaries_id)
                                            ).first()
    if db_category is None:
        db.close()
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        if key == 'author':
            continue
        if value is not None and hasattr(Category, key):
            setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    db.close()

    delete_cache_from_redis(f'all_categories_{category.bestiaries_id}', str(category.author))
    delete_cache_from_redis(f'category_{category.author}', str(category_id))
    return db_category


# ___________________________ entities ________________________________


# Создание новой сущности
@app_v1.post("/entities/", response_model=EntityOut, tags=["entities"])
def create_entity(entity: EntityCreate):
    db = SessionLocal()
    entity_dict = {k: v for k, v in entity.dict().items() if k != "author"}
    db_entity = Entity(**entity_dict)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    db.close()

    delete_cache_from_redis(f'all_entities_{entity.bestiaries_id}', str(entity.author))
    return db_entity


# Получение списка всех сущностей
@app_v1.get("/entities/", response_model=List[EntityOut], tags=["entities"])
def read_entities(entity: EntityGetIn):
    cached_data = get_cache_from_redis('all_categories', str(entity.author))
    if cached_data:
        return cached_data
    db = SessionLocal()
    bestiary = db.query(Bestiaries).filter(and_(Bestiaries.id == entity.bestiaries_id,
                                                Bestiaries.author == entity.author,
                                                Bestiaries.is_deleted == False)
                                           ).first()
    if bestiary is None:
        db.close()
        raise HTTPException(status_code=404, detail="Bestiary not found")
    entities = db.query(Entity).filter(Entity.bestiaries_id == entity.bestiaries_id).all()
    db.close()

    set_cache(f'all_entities_{entity.bestiaries_id}', str(entity.author), entities)
    return entities


# Получение сущности по ID
@app_v1.get("/entities/{entity_id}", response_model=EntityOut, tags=["entities"])
def read_entity(entity_id: int, entity: EntityGetIn):
    cached_data = get_cache_from_redis(f'entity_{entity.author}', str(entity_id))
    if cached_data:
        return cached_data
    db = SessionLocal()
    db_entity = db.query(Entity).filter(and_(Entity.id == entity_id,
                                             Entity.bestiaries_id == entity.bestiaries_id)
                                        ).first()
    db.close()
    if db_entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")

    set_cache(f'entity_{entity.author}', str(entity_id), db_entity)
    return db_entity


# Удаление сущности по ID
@app_v1.delete("/entities/{entity_id}", response_model=EntityOut, tags=["entities"])
def delete_entity(entity_id: int, entity: EntityGetIn):
    db = SessionLocal()
    db_entity = db.query(Entity).filter(and_(Entity.id == entity_id,
                                             Entity.bestiaries_id == entity.bestiaries_id)
                                        ).first()
    if db_entity is None:
        db.close()
        raise HTTPException(status_code=404, detail="Entity not found")
    db.delete(db_entity)
    db.commit()
    db.close()

    delete_cache_from_redis(f'all_entities_{entity.bestiaries_id}', str(entity.author))
    delete_cache_from_redis(f'entity_{entity.author}', str(entity_id))
    return db_entity


# Изменение категории по ID
@app_v1.put("/entities/{entity_id}", response_model=EntityOut, tags=["entities"])
def update_entity(entity_id: int, entity: EntityUpdate):
    # TODO тут проверка по jwt токен
    db = SessionLocal()
    db_entity = db.query(Entity).filter(and_(Entity.id == entity_id,
                                             Entity.bestiaries_id == entity.bestiaries_id)
                                        ).first()
    if db_entity is None:
        db.close()
        raise HTTPException(status_code=404, detail="Entity not found")
    for key, value in entity.dict().items():
        if key == 'author':
            continue
        if value is not None and hasattr(Entity, key):
            setattr(db_entity, key, value)

    db.commit()
    db.refresh(db_entity)
    db.close()

    delete_cache_from_redis(f'all_entities_{entity.bestiaries_id}', str(entity.author))
    delete_cache_from_redis(f'entity_{entity.author}', str(entity_id))
    return db_entity
