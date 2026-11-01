from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notification Service",
    description="Microservice for managing insurance notifications",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Insurance Notification Service",
        "status": "Running"
    }


# Create notification
@app.post(
    "/notifications",
    response_model=schemas.NotificationResponse,
    status_code=201
)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):
    new_notification = models.Notification(**notification.model_dump())

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


# Retrieve all notifications
@app.get(
    "/notifications",
    response_model=list[schemas.NotificationResponse]
)
def get_notifications(db: Session = Depends(get_db)):
    return db.query(models.Notification).all()


# Retrieve notification by ID
@app.get(
    "/notifications/{notification_id}",
    response_model=schemas.NotificationResponse
)
def get_notification(notification_id: int, db: Session = Depends(get_db)):

    notification = db.query(models.Notification).filter(
        models.Notification.notification_id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


# Mark notification as read
@app.patch(
    "/notifications/{notification_id}/read",
    response_model=schemas.NotificationResponse
)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db)
):

    notification = db.query(models.Notification).filter(
        models.Notification.notification_id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification