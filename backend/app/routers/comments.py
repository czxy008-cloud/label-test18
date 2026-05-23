from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/comments", tags=["评论"])


@router.get("/article/{article_id}", response_model=schemas.PaginatedComments)
def get_article_comments(
    article_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    comments, total = crud.get_article_comments(db, article_id=article_id, skip=skip, limit=page_size)
    result = []
    for comment in comments:
        result.append(_build_comment_with_replies(comment))
    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("", response_model=schemas.PaginatedComments)
def list_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_approved: Optional[bool] = None,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    comments, total = crud.get_all_comments(db, skip=skip, limit=page_size, is_approved=is_approved)
    result = []
    for comment in comments:
        result.append(_build_comment_with_replies(comment))
    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    article_id: int = Query(...),
    comment: schemas.CommentCreate = ...,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    if comment.parent_id:
        parent_comment = crud.get_comment_by_id(db, comment_id=comment.parent_id)
        if not parent_comment:
            raise HTTPException(status_code=404, detail="父评论不存在")
        if parent_comment.article_id != article_id:
            raise HTTPException(status_code=400, detail="父评论不属于该文章")
    return crud.create_comment(db, comment=comment, article_id=article_id, user_id=current_user.id)


@router.put("/{comment_id}/approve", response_model=schemas.CommentResponse)
def approve_comment(
    comment_id: int,
    update: schemas.CommentAdminUpdate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    return crud.update_comment(db, comment_id=comment_id, comment_update=schemas.CommentUpdate(is_approved=update.is_approved))


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此评论")
    crud.delete_comment(db, comment_id=comment_id)


def _build_comment_with_replies(comment: models.Comment) -> dict:
    result = {
        "id": comment.id,
        "content": comment.content,
        "is_approved": comment.is_approved,
        "user": comment.user,
        "parent_id": comment.parent_id,
        "article_id": comment.article_id,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "replies": []
    }
    if comment.replies:
        for reply in comment.replies:
            if reply.is_approved:
                result["replies"].append(_build_comment_with_replies(reply))
    return result
