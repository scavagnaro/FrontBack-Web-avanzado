from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        name=event.name,
        image=event.image,
        sector=event.sector,
        address=event.address,
        phone=event.phone,
        email=event.email,
        additional_info=event.additional_info,
        city_id=event.city_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: UUID):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_event_comments(db: Session, event_id: UUID):
    return db.query(models.Comment).filter(models.Comment.event_id == event_id).all()


def update_event(db: Session, event_id: UUID, event: schemas.Event):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_event.name = event.name
    db_event.image = event.image
    db_event.sector = event.sector
    db_event.address = event.address
    db_event.phone = event.phone
    db_event.email = event.email
    db_event.additional_info = event.additional_info
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: UUID):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db.delete(db_event)
    db.commit()
    return db_event


def save_image(db: Session, event_id: UUID, image_url: str):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_event.image = image_url
    db.commit()
    db.refresh(db_event)
    return db_event
