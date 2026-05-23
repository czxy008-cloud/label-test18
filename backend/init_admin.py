"""
初始化脚本：创建或重置管理员账户

使用方法：
    python init_admin.py                  # 使用默认密码 admin123
    python init_admin.py --password 你的密码  # 使用自定义密码
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import argparse


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')


def init_admin(password: str = "admin123"):
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        
        if admin:
            admin.password_hash = hash_password(password)
            admin.is_admin = True
            admin.is_active = True
            print(f"✓ 管理员账户已更新，密码: {password}")
        else:
            admin = models.User(
                username="admin",
                email="admin@blog.com",
                password_hash=hash_password(password),
                is_admin=True,
                is_active=True,
                bio="系统管理员"
            )
            db.add(admin)
            print(f"✓ 管理员账户已创建，密码: {password}")
        
        db.commit()
        print("✓ 操作完成！请使用 admin 账号登录")
        
    except Exception as e:
        db.rollback()
        print(f"✗ 操作失败: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化管理员账户")
    parser.add_argument("--password", "-p", default="admin123", help="管理员密码 (默认: admin123)")
    args = parser.parse_args()
    
    print("正在初始化管理员账户...")
    init_admin(args.password)
