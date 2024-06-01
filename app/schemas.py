from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    image: str | None = None
    sector: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    additional_info: str | None = None
    city_id: UUID | None = None


class Event(EventBase):
    id: UUID
    image: str | None
    sector: str | None
    address: str | None
    phone: str | None
    email: str | None
    additional_info: str | None
    city_id: UUID | None

    class Config:
        orm_mode = True


class EventUpdate(EventBase):
    image: str | None = None
    sector: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    additional_info: str | None = None
    city_id: UUID | None = None

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    message: str
    rating: float


class CommentCreate(CommentBase):
    event_id: UUID


class Comment(CommentBase):
    id: UUID

    class Config:
        orm_mode = True


class CommentUpdate(CommentBase):
    message: str | None = None
    rating: float | None = None

    class Config:
        orm_mode = True


class IndicatorBase(BaseModel):
    name: str
    value: float


class IndicatorCreate(IndicatorBase):
    event_id: UUID


class Indicator(IndicatorBase):
    id: UUID

    class Config:
        orm_mode = True


class IndicatorUpdate(IndicatorBase):
    name: str | None = None
    value: float | None = None

    class Config:
        orm_mode = True


class CityBase(BaseModel):
    name: str
    image: str


class CityCreate(CityBase):

    class Config:
        orm_mode = True


class City(CityBase):
    id: UUID

    class Config:
        orm_mode = True


class CityUpdate(CityBase):
    name: str | None = None
    image: str | None = None

    class Config:
        orm_mode = True
