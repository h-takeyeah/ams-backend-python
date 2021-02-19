from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
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


@app.post('/accesslogs', response_model=schemas.AccessLog, status_code=201)
def create_accesslog(log: schemas.AccessLog, db: Session = Depends(get_db)):
    return crud.create_accesslog(db, log=log)


@app.get('/accesslogs', response_model=List[schemas.AccessLog])
def read_accesslogs(
    begin: datetime = None, end: datetime = None,
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    if begin and end:
        logs = crud.get_accesslogs_with_duration(
            db, begin=begin, end=end, skip=skip, limit=limit)
    else:
        logs = crud.get_accesslogs(db, skip=skip, limit=limit)
    return logs


@app.get('/room', response_model=List[schemas.InRoomUser])
def read_inroomusers(db: Session = Depends(get_db)):
    return crud.get_inroomusers(db)


@app.get('/room/{parsed_id}', response_model=schemas.InRoomUser)
def read_inroomuser(parsed_id: int, db: Session = Depends(get_db)):
    user = crud.get_inroomuser(db, user_id=parsed_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f'User({parsed_id}) is not in the room')
    return user


@app.post('/room', response_model=schemas.InRoomUser, status_code=201)
def create_inroomuser(user: schemas.InRoomUserBase, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_inroomuser(db, user=user)
    except:
        raise HTTPException(
            status_code=409, detail=f'Conflict! User({user.id}) is already in the room')
    return db_user


@app.delete('/room/{parsed_id}', response_model=None, status_code=204)
def delete_and_move_inroomuser(parsed_id: int, db: Session = Depends(get_db)):
    """
    1. copy(if exists)
    2. delete original
    3. paste
    """
    user = crud.get_inroomuser(db, user_id=parsed_id)  # 1. copy(if exists)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f'Cannot delete non-existent User({parsed_id})')
    crud.delete_inroomuser(db, user=user)  # 2. delele

    log = schemas.AccessLog(
        student_id=user.id, entered_at=user.entered_at, exited_at=datetime.now())
    crud.create_accesslog(db, log)  # 3. paste
    return
