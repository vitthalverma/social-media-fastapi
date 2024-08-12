from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends, HTTPException, APIRouter, status
from app import schemas, models
from app.database import get_db
from app import oauth2

router = APIRouter(
    tags= ['Post']
)


@router.get('/posts',  response_model= list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).all()
    return posts


@router.get('/posts/{post_id}',  response_model=schemas.PostOut)
async def get_post(post_id: int, db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user) ):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail= f"Post with id {post_id} not found")
    return post


@router.post('/posts', response_model=schemas.PostResponseSchema)
async def create_post(post: schemas.PostCreateSchema , db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user)):
    new_post =  models.Post(owner_id = current_user_creds.id,  **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/posts/{post_id}')
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    if post.owner_id != current_user_creds.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= 'Not authorized to perfrom requested action')
    db.delete(post)
    db.commit()
    return {'message': f'Post with id {post_id} deleted'}

@router.put('/posts/{post_id}', response_model=schemas.PostResponseSchema)
async def update_post(post_id: int,updated_post: schemas.PostUpdateSchema, db: Session = Depends(get_db), current_user_creds: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise  HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    if post.owner_id != current_user_creds.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= 'Not authorized to perfrom requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()