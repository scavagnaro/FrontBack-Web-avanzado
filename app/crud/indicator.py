from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas


def create_indicator(db: Session, indicator: schemas.IndicatorCreate):
    db_indicator = models.Indicator(
        name=indicator.name, value=indicator.value, event_id=indicator.event_id
    )
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator


def get_indicators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Indicator).offset(skip).limit(limit).all()


def get_indicator(db: Session, indicator_id: UUID):
    return (
        db.query(models.Indicator).filter(models.Indicator.id == indicator_id).first()
    )


def update_indicator(db: Session, indicator_id: UUID, indicator: schemas.Indicator):
    db_indicator = (
        db.query(models.Indicator).filter(models.Indicator.id == indicator_id).first()
    )
    db_indicator.name = indicator.name
    db_indicator.value = indicator.value
    db.commit()
    db.refresh(db_indicator)
    return db_indicator


def delete_indicator(db: Session, indicator_id: UUID):
    db_indicator = (
        db.query(models.Indicator).filter(models.Indicator.id == indicator_id).first()
    )
    db.delete(db_indicator)
    db.commit()
    return db_indicator
