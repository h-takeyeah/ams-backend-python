from datetime import datetime
from typing import List, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def get_accesslogs(db: Session, skip: int = 0, limit: int = 100) -> List:
    return db.query(models.AccessLog).offset(skip).limit(limit).all()


def get_accesslogs_with_duration(
    db: Session, begin: datetime, end: datetime, skip: int = 0, limit: int = 100
) -> List:
    return db.query(models.AccessLog).filter(
        models.AccessLog.entered_at >= begin, models.AccessLog.exited_at <= end
    ).offset(skip).limit(limit).all()


def create_accesslog(db: Session, log: schemas.AccessLog) -> models.AccessLog:
    db_log = models.AccessLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_inroomuser(db: Session, user_id: int) -> Union[models.InRoomUser, None]:
    return db.query(models.InRoomUser).filter(models.InRoomUser.id == user_id).first()


def get_inroomusers(db: Session) -> List:
    return db.query(models.InRoomUser).all()


def create_inroomuser(db: Session, user: schemas.InRoomUserBase) -> models.InRoomUser:
    db_user = models.InRoomUser(**user.dict())  # Just `id` will be passed
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as ie:
        raise ie
    db.refresh(db_user)
    return db_user


def delete_inroomuser(db: Session, user: schemas.InRoomUser):
    db_user = db.query(models.InRoomUser).filter(
        models.InRoomUser.id == user.id).first()
    db.delete(db_user)
    db.commit()
    return
