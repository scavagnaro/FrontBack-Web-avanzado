from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        message=comment.message, rating=comment.rating, event_id=comment.event_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: UUID):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def update_comment(db: Session, comment_id: UUID, comment: schemas.Comment):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    db_comment.message = comment.message
    db_comment.rating = comment.rating
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: UUID):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    db.delete(db_comment)
    db.commit()
    return db_comment
