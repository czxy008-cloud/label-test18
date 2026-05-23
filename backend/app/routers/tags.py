from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_admin_user

router = APIRouter(prefix="/api/tags", tags=["标签"])


@router.get("", response_model=List[schemas.TagResponse])
def list_tags(db: Session = Depends(get_db)):
    return crud.get_all_tags(db)


@router.get("/{tag_id}", response_model=schemas.TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag_by_id(db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return db_tag


@router.post("", response_model=schemas.TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: schemas.TagCreate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_tag = crud.get_tag_by_name(db, name=tag.name)
    if db_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标签已存在"
        )
    return crud.create_tag(db, tag=tag)


@router.put("/{tag_id}", response_model=schemas.TagResponse)
def update_tag(
    tag_id: int,
    tag_update: schemas.TagUpdate,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    db_tag = crud.get_tag_by_id(db, tag_id=tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return crud.update_tag(db, tag_id=tag_id, tag_update=tag_update)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    current_user: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_tag(db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签不存在")
