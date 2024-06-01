from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

import uuid


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )

    name = Column(String)
    image = Column(String)

    sector = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    additional_info = Column(String)

    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"))
    city = relationship("City", back_populates="events")

    comments = relationship("Comment", back_populates="event")

    indicators = relationship("Indicator", back_populates="event")


class City(Base):

    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, unique=True, index=True)
    image = Column(String)


    events = relationship("Event", back_populates="city")  

class Comment(Base):

    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    message = Column(String)
    rating = Column(Float)

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    event = relationship("Event", back_populates="comments")

class Indicator(Base):
    
        __tablename__ = "indicators"
    
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

        name = Column(String)
        value = Column(String)
        icon = Column(String)
        reviews = Column(Integer)

        event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
        event = relationship("Event", back_populates="indicators")



