from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, articles, tags, comments

app = FastAPI(
    title="个人博客内容管理系统 API",
    description="基于 FastAPI + PostgreSQL 的博客系统后端 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(tags.router)
app.include_router(comments.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "博客系统 API 运行正常"}
