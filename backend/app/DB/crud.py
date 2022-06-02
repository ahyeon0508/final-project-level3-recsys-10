# DB에 연결하여 직접적으로 Create(생성), Read(읽기), Update(갱신), Delete(삭제) 와 관련한 모듈들은 담당하는 곳
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models
from . import schemas

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_profile_name(db: Session, profile_name: str):
    return db.query(models.User).filter(models.User.profile_name == profile_name).first()

def get_beer(db: Session, beer_id: int):
    return db.query(models.Beer).filter(models.Beer.beer_id == beer_id).first()

def get_popular_review(db: Session):
    s = """
    select beer_id, count(beer_id), avg(review_score)
    from review
    group by beer_id
    order by avg(review_score) desc
    """
    return db.execute(s).all()

def get_beer_review(db:Session, beer_id: int) -> List:
    s= f"""
    select u.profile_name, r.review_score, r.appearance, r.aroma, r.palate, r.taste, r.review_text
    from review as r
    join reviewer as u
    on r.user_id = u.user_id
    where r.beer_id = {beer_id};
    """
    review = db.execute(s).all()
    return review

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"    
    max_id_before = db.query(func.max(models.User.user_id)).scalar()
    db_user = models.User(
                    user_id=int(max_id_before + 1), 
                    password=fake_hashed_password, 
                    profile_name=user.profile_name,
                    gender=user.gender, 
                    birth=user.birth
                )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user