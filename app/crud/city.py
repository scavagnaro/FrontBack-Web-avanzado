from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, image=city.image)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: UUID):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_events(db: Session, city_id: UUID):
    return db.query(models.Event).filter(models.Event.city_id == city_id).all()


def update_city(db: Session, city_id: UUID, city: schemas.City):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    db_city.name = city.name
    db_city.image = city.image
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: UUID):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    db.delete(db_city)
    db.commit()
    return db_city
