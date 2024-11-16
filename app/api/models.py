import datetime

from pydantic import BaseModel
from typing import List, Optional


class BestiariesCreate(BaseModel):
    name: str


class BestiariesOut(BaseModel):
    id: int
    name: str
    author: int
    date_creation: datetime.datetime
    latest_update: datetime.datetime
    is_star: bool
    average_rating: float
    count_views: int
    src_icon: str
    src_background_img: str
    description: str


class BestiariesUpdate(BaseModel):
    name: Optional[str] = None
    is_star: Optional[bool] = None
    src_icon: Optional[str] = None
    src_background_img: Optional[str] = None
    description: Optional[str] = None


# ___________________________ categories ________________________________


class CategoryGetIn(BaseModel):
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
    bestiaries_id: int

    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    img_name: Optional[str] = None
    background_color: Optional[str] = None
