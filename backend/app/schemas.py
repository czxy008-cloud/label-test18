from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = "#1890ff"


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class TagResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    color: str
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    summary: Optional[str] = None
    content: str
    cover_image: Optional[str] = None
    is_published: bool = True
    tag_ids: List[int] = []


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    is_published: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class ArticleListResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    views_count: int
    likes_count: int
    is_published: bool
    author: UserResponse
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleDetailResponse(ArticleListResponse):
    content: str


class PaginatedArticles(BaseModel):
    items: List[ArticleListResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None
    is_approved: Optional[bool] = None


class CommentUser(BaseModel):
    id: int
    username: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    content: str
    is_approved: bool
    user: CommentUser
    parent_id: Optional[int] = None
    article_id: int
    created_at: datetime
    updated_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class PaginatedComments(BaseModel):
    items: List[CommentResponse]
    total: int
    page: int
    page_size: int


class CommentAdminUpdate(BaseModel):
    is_approved: bool
