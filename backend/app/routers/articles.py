from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_user

router = APIRouter(prefix="/api/articles", tags=["文章"])


@router.get("", response_model=schemas.PaginatedArticles)
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    is_published: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    articles, total = crud.get_articles(
        db, skip=skip, limit=page_size,
        tag_id=tag_id, search=search,
        is_published=is_published
    )
    total_pages = (total + page_size - 1) // page_size
    return {
        "items": articles,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{article_id}", response_model=schemas.ArticleDetailResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    crud.increment_article_views(db, article_id=article_id)
    return db_article


@router.get("/slug/{slug}", response_model=schemas.ArticleDetailResponse)
def get_article_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_slug(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    crud.increment_article_views(db, article_id=db_article.id)
    return db_article


@router.post("", response_model=schemas.ArticleDetailResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article: schemas.ArticleCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_article(db, article=article, author_id=current_user.id)


@router.put("/{article_id}", response_model=schemas.ArticleDetailResponse)
def update_article(
    article_id: int,
    article_update: schemas.ArticleUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权修改此文章")
    return crud.update_article(db, article_id=article_id, article_update=article_update)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此文章")
    crud.delete_article(db, article_id=article_id)


@router.post("/{article_id}/like")
def like_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    crud.increment_article_likes(db, article_id=article_id)
    return {"message": "点赞成功", "likes_count": db_article.likes_count + 1}
