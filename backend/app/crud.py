from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app import models, schemas
from app.auth import hash_password


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    slug = user.username.lower().replace(" ", "-")
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user_by_id(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[models.User], int]:
    query = db.query(models.User)
    total = query.count()
    users = query.order_by(models.User.created_at.desc()).offset(skip).limit(limit).all()
    return users, total


def create_tag(db: Session, tag: schemas.TagCreate) -> models.Tag:
    slug = tag.name.lower().replace(" ", "-")
    db_tag = models.Tag(
        name=tag.name,
        slug=slug,
        description=tag.description,
        color=tag.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag_by_id(db: Session, tag_id: int) -> Optional[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def get_tag_by_name(db: Session, name: str) -> Optional[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def get_tag_by_slug(db: Session, slug: str) -> Optional[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.slug == slug).first()


def get_all_tags(db: Session) -> List[models.Tag]:
    return db.query(models.Tag).order_by(models.Tag.name).all()


def update_tag(db: Session, tag_id: int, tag_update: schemas.TagUpdate) -> Optional[models.Tag]:
    db_tag = get_tag_by_id(db, tag_id)
    if db_tag:
        update_data = tag_update.model_dump(exclude_unset=True)
        if "name" in update_data:
            update_data["slug"] = update_data["name"].lower().replace(" ", "-")
        for key, value in update_data.items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> bool:
    db_tag = get_tag_by_id(db, tag_id)
    if db_tag:
        db.delete(db_tag)
        db.commit()
        return True
    return False


def create_article(db: Session, article: schemas.ArticleCreate, author_id: int) -> models.Article:
    slug = article.title.lower().replace(" ", "-") + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
    db_article = models.Article(
        title=article.title,
        slug=slug,
        summary=article.summary,
        content=article.content,
        cover_image=article.cover_image,
        author_id=author_id,
        is_published=article.is_published
    )
    if article.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(article.tag_ids)).all()
        db_article.tags = tags
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article_by_id(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_article_by_slug(db: Session, slug: str) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.slug == slug).first()


def get_articles(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    is_published: Optional[bool] = None
) -> tuple[List[models.Article], int]:
    query = db.query(models.Article)
    if is_published is not None:
        query = query.filter(models.Article.is_published == is_published)
    if search:
        query = query.filter(
            or_(
                models.Article.title.ilike(f"%{search}%"),
                models.Article.summary.ilike(f"%{search}%"),
                models.Article.content.ilike(f"%{search}%")
            )
        )
    if tag_id:
        query = query.join(models.Article.tags).filter(models.Tag.id == tag_id)
    total = query.count()
    articles = query.order_by(models.Article.created_at.desc()).offset(skip).limit(limit).all()
    return articles, total


def increment_article_views(db: Session, article_id: int) -> None:
    db_article = get_article_by_id(db, article_id)
    if db_article:
        db_article.views_count += 1
        db.commit()


def increment_article_likes(db: Session, article_id: int) -> None:
    db_article = get_article_by_id(db, article_id)
    if db_article:
        db_article.likes_count += 1
        db.commit()


def update_article(db: Session, article_id: int, article_update: schemas.ArticleUpdate) -> Optional[models.Article]:
    db_article = get_article_by_id(db, article_id)
    if db_article:
        update_data = article_update.model_dump(exclude_unset=True)
        tag_ids = update_data.pop("tag_ids", None)
        if "title" in update_data:
            update_data["slug"] = update_data["title"].lower().replace(" ", "-") + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        for key, value in update_data.items():
            setattr(db_article, key, value)
        if tag_ids is not None:
            tags = db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()
            db_article.tags = tags
        db.commit()
        db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int) -> bool:
    db_article = get_article_by_id(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False


def create_comment(db: Session, comment: schemas.CommentCreate, article_id: int, user_id: int) -> models.Comment:
    db_comment = models.Comment(
        content=comment.content,
        article_id=article_id,
        user_id=user_id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment_by_id(db: Session, comment_id: int) -> Optional[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_article_comments(
    db: Session,
    article_id: int,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[models.Comment], int]:
    query = db.query(models.Comment).filter(
        and_(
            models.Comment.article_id == article_id,
            models.Comment.parent_id == None,
            models.Comment.is_approved == True
        )
    )
    total = query.count()
    comments = query.order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()
    return comments, total


def get_all_comments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    is_approved: Optional[bool] = None
) -> tuple[List[models.Comment], int]:
    query = db.query(models.Comment)
    if is_approved is not None:
        query = query.filter(models.Comment.is_approved == is_approved)
    total = query.count()
    comments = query.order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()
    return comments, total


def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate) -> Optional[models.Comment]:
    db_comment = get_comment_by_id(db, comment_id)
    if db_comment:
        update_data = comment_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int) -> bool:
    db_comment = get_comment_by_id(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return True
    return False


def build_comment_tree(comments: List[models.Comment]) -> List[dict]:
    comment_map = {}
    roots = []
    for comment in comments:
        comment_dict = {
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
        comment_map[comment.id] = comment_dict
        if comment.parent_id is None:
            roots.append(comment_dict)
        else:
            if comment.parent_id in comment_map:
                comment_map[comment.parent_id]["replies"].append(comment_dict)
    return roots
