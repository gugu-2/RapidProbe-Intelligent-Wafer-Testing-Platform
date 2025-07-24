from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import User, UserCreate
from ..models import User as DBUser
from ..utils import hash_password
from ..routers.auth import get_current_admin

router = APIRouter()

@router.post("/", response_model=User, dependencies=[Depends(get_current_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = DBUser(username=user.username, hashed_pw=hashed_pw, role=user.role)
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[User], dependencies=[Depends(get_current_admin)])
def list_users(db: Session = Depends(get_db)):
    return db.query(DBUser).all()
