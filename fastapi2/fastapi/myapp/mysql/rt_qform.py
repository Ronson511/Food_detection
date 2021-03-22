from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
# from . import models
# from . import crud
# from . import schemas
from .database import SessionLocal, engine
# import crud, models, schemas
# from  database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/{user_id}', response_model=schemas.qustForm)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post('/', response_model=schemas.qustForm)
def create_user(user: schemas.qustFormCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

