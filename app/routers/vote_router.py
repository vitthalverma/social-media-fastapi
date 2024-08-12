from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, status
from app import schemas, models
from app.database import get_db
from app import oauth2

router = APIRouter(prefix= "/vote" , tags= ["Vote"])

@router.post('/', status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.VoteSchema, db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user_creds.id).first()
    if(vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted on this post")
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user_creds.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)    
            return {'message': "successfully added vote"}       
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has not voted on this post")
        db.delete(found_vote)
        db.commit()
        return {'message': "Successfully removed vote"}        
 
    
  
  
  
  
  
  

    
  