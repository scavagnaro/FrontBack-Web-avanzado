from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Response
from sqlalchemy.orm import Session
from uuid import UUID

from . import crud, schemas, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.post("/users/", response_model=schemas.User, tags=["users"], status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}", response_model=schemas.User, tags=["users"])
def update_user(user_id: UUID, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.user.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@app.post(
    "/events/",
    response_model=schemas.Event,
    status_code=status.HTTP_201_CREATED,
    tags=["events"],
)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.event.create_event(db=db, event=event)


@app.patch("/events/{event_id}/image", response_model=schemas.Event, tags=["events"])
async def upload_event_image(
    event_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    upload_image_url: str = await crud.image.upload_image(file=file)
    if upload_image_url is None or not upload_image_url.startswith("http"):
        return Response(
            status_code=400,
            content={"Message": "Image upload failed", "exception": upload_image_url},
        )
    db_event = crud.event.save_image(db, event_id=event_id, image_url=upload_image_url)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.get("/events/", response_model=list[schemas.Event], tags=["events"])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.event.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def read_event(event_id: UUID, db: Session = Depends(get_db)):
    db_event = crud.event.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.patch("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def update_event(
    event_id: UUID, event: schemas.EventUpdate, db: Session = Depends(get_db)
):
    db_event = crud.event.update_event(db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.delete("/events/{event_id}", tags=["events"])
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    db_event = crud.event.delete_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}


@app.post(
    "/comments/",
    response_model=schemas.Comment,
    status_code=status.HTTP_201_CREATED,
    tags=["comments"],
)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.comment.create_comment(db=db, comment=comment)


@app.get(
    "/comments/",
    response_model=list[schemas.Comment],
    status_code=status.HTTP_200_OK,
    tags=["comments"],
)
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.comment.get_comments(db, skip=skip, limit=limit)
    return comments


@app.get("/comments/{comment_id}", response_model=schemas.Comment, tags=["comments"])
def read_comment(comment_id: UUID, db: Session = Depends(get_db)):
    db_comment = crud.comment.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.patch("/comments/{comment_id}", response_model=schemas.Comment, tags=["comments"])
def update_comment(
    comment_id: UUID, comment: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    db_comment = crud.comment.update_comment(db, comment_id=comment_id, comment=comment)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.delete("/comments/{comment_id}", tags=["comments"])
def delete_comment(comment_id: UUID, db: Session = Depends(get_db)):
    db_comment = crud.comment.delete_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted"}


@app.post(
    "/cities/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
    tags=["cities"],
)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.city.create_city(db=db, city=city)


@app.get("/cities/", response_model=list[schemas.City], tags=["cities"])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.city.get_cities(db, skip=skip, limit=limit)
    return cities


@app.get("/cities/{city_id}", response_model=schemas.City, tags=["cities"])
def read_city(city_id: UUID, db: Session = Depends(get_db)):
    db_city = crud.city.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.patch("/cities/{city_id}", response_model=schemas.City, tags=["cities"])
def update_city(city_id: UUID, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.city.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}", tags=["cities"])
def delete_city(city_id: UUID, db: Session = Depends(get_db)):
    db_city = crud.city.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted"}


@app.post(
    "/indicator/",
    response_model=schemas.Indicator,
    status_code=status.HTTP_201_CREATED,
    tags=["indicators"],
)
def create_indicator(indicator: schemas.IndicatorCreate, db: Session = Depends(get_db)):
    return crud.indicator.create_indicator(db=db, indicator=indicator)


@app.get("/indicators/", response_model=list[schemas.Indicator], tags=["indicators"])
def read_indicators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    indicators = crud.indicator.get_indicators(db, skip=skip, limit=limit)
    return indicators


@app.get(
    "/indicators/{indicator_id}", response_model=schemas.Indicator, tags=["indicators"]
)
def read_indicator(indicator_id: UUID, db: Session = Depends(get_db)):
    db_indicator = crud.indicator.get_indicator(db, indicator_id=indicator_id)
    if db_indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return db_indicator


@app.patch(
    "/indicators/{indicator_id}", response_model=schemas.Indicator, tags=["indicators"]
)
def update_indicator(
    indicator_id: UUID,
    indicator: schemas.IndicatorUpdate,
    db: Session = Depends(get_db),
):
    db_indicator = crud.indicator.update_indicator(
        db, indicator_id=indicator_id, indicator=indicator
    )
    if db_indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return db_indicator


@app.delete("/indicators/{indicator_id}", tags=["indicators"])
def delete_indicator(indicator_id: UUID, db: Session = Depends(get_db)):
    db_indicator = crud.indicator.delete_indicator(db, indicator_id=indicator_id)
    if db_indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return {"message": "Indicator deleted"}
