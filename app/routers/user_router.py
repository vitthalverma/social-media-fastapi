from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, status
from app import schemas, models
from app.database import get_db
from app.utils import hashPassword

router = APIRouter(
    tags= ['Users']
)

@router.post('/users', response_model= schemas.UserResponse)
async def create_user(user: schemas.CreateUserSchema, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hashPassword(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
    
@router.get('/users/{user_id}', response_model= schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    