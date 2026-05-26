from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
import random
from app.database import get_db
from app import schemas, crud, models
from app.auth import verify_password, create_access_token, hash_password
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])

RESET_CODE_EXPIRE_MINUTES = 15


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册"
        )
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user_credentials.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if not verify_password(user_credentials.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户已被禁用"
        )
    
    expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    if user_credentials.remember_me:
        expire_minutes = 7 * 24 * 60
    
    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = create_access_token(
        data={"user_id": db_user.id, "username": db_user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=request.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱未注册"
        )
    
    code = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_CODE_EXPIRE_MINUTES)
    
    db.query(models.PasswordResetCode).filter(
        models.PasswordResetCode.email == request.email
    ).delete()
    
    reset_code = models.PasswordResetCode(
        email=request.email,
        code=code,
        expires_at=expires_at
    )
    db.add(reset_code)
    db.commit()
    
    print(f"验证码 {code} 已发送到邮箱 {request.email}")
    return {"message": "验证码已发送到您的邮箱"}


@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_code = db.query(models.PasswordResetCode).filter(
        models.PasswordResetCode.email == request.email
    ).order_by(models.PasswordResetCode.created_at.desc()).first()
    
    if not reset_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
    if reset_code.code != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
    if reset_code.expires_at < datetime.now(timezone.utc):
        db.delete(reset_code)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码已过期，请重新获取"
        )
    
    db_user = crud.get_user_by_email(db, email=request.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    db_user.password_hash = hash_password(request.new_password)
    db.commit()
    
    db.delete(reset_code)
    db.commit()
    
    return {"message": "密码重置成功"}
