from sqlalchemy.orm import Session

from . import models, schemas
# import .models, .schemas


def get_user(db: Session, user_id: int):
    return db.query(models.qustForm).filter(models.qustForm.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    db.query(models.qustForm)
    return db.query(models.qustForm).filter(models.qustForm.email == email).first()


def create_user(db: Session, user: schemas.qustFormCreate):
    db_user = models.qustForm(
        username =  user.username,
        email  =    user.email,
        gender =    user.gender,
        height =    user.height,
        weight =    user.weight,
        target =    user.target,
        age_range = user.age_range,
        work_type = user.work_type,
        dining    = user.dining,
        cuisine   = user.cuisine,
        cook_tool = user.cook_tool,
        cook_time = user.cook_time,
        allergy   = user.allergy
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
