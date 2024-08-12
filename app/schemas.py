from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateSchema(PostBaseSchema):
    pass

class PostUpdateSchema(PostBaseSchema):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
 
class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

class PostOut(BaseModel):
    Post: PostResponseSchema
    votes: int    
    
 ################################################################
 #################### Users ##############################

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str 
    

  
class UserLoginInput(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    id: str | None = None    
    
    
################################################################
 #################### Votes ##############################

class VoteSchema(BaseModel):
    post_id: int
    direction: int = Field(ge=0, le=1)