from sqlalchemy.orm import Session
from app import schemas, models, oauth2
from fastapi import Depends, HTTPException, APIRouter, status
from app.database import get_db
from app.utils import verifyPassword


router = APIRouter(tags= ['Authentication'])


@router.post('/users/login', response_model= schemas.Token)
async def login(req: schemas.UserLoginInput, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    if not verifyPassword(user.password, req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = oauth2.create_access_token({'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
