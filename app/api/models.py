import datetime

from pydantic import BaseModel
from typing import List, Optional


class BestiariesGetIn(BaseModel):
    author: int


class BestiariesCreate(BaseModel):
    name: str
    author: int


class BestiariesOut(BaseModel):
    id: int
    name: str
    author: int
    date_creation: datetime.datetime
    latest_update: datetime.datetime
    is_star: bool


class BestiariesUpdate(BaseModel):
    author: int
    name: Optional[str] = None
    is_star: Optional[bool] = None


# ___________________________ categories ________________________________


class CategoryGetIn(BaseModel):
    author: int
    bestiaries_id: int


class CategoryCreate(BaseModel):
    bestiaries_id: int
    name: str
    background_img: str
    background_color: str


class CategoryOut(BaseModel):
    id: int
    bestiaries_id: int
    name: str
    background_img: str
    background_color: str


class CategoryUpdate(BaseModel):
    author: int
    bestiaries_id: int

    name: Optional[str] = None
    background_img: Optional[str] = None
    background_color: Optional[str] = None


# ___________________________ entities ________________________________


class EntityCreate(BaseModel):
    bestiaries_id: int
    name: str
    description: str
    category_id: int
    img_name: str
    background_color: str


class EntityGetIn(BaseModel):
    author: int
    bestiaries_id: int


class EntityOut(BaseModel):
    id: int
    bestiaries_id: int
    name: str
    description: str
    category_id: int
    img_name: str
    background_color: str


class EntityUpdate(BaseModel):
    author: int
    bestiaries_id: int

    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    img_name: Optional[str] = None
    background_color: Optional[str] = None