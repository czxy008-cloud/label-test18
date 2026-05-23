# 个人博客内容管理系统

基于 FastAPI + Vue3 的全栈博客系统。

## 技术栈

### 后端
- **Python 3.10+**
- **FastAPI** - 高性能 Web 框架
- **PostgreSQL** - 关系型数据库
- **SQLAlchemy** - ORM 框架
- **Pydantic** - 数据验证
- **JWT** - 身份认证

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Element Plus** - UI 组件库
- **Axios** - HTTP 客户端
- **WangEditor** - 富文本编辑器

## 项目结构

```
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── routers/         # API 路由
│   │   │   ├── auth.py      # 认证路由
│   │   │   ├── users.py     # 用户路由
│   │   │   ├── articles.py  # 文章路由
│   │   │   ├── tags.py      # 标签路由
│   │   │   └── comments.py  # 评论路由
│   │   ├── __init__.py
│   │   ├── config.py        # 配置文件
│   │   ├── database.py      # 数据库连接
│   │   ├── models.py        # 数据模型
│   │   ├── schemas.py       # Pydantic 模型
│   │   ├── crud.py          # CRUD 操作
│   │   └── auth.py          # 认证逻辑
│   ├── requirements.txt     # Python 依赖
│   ├── .env.example         # 环境变量示例
│   └── main.py              # 应用入口
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── api/             # API 接口
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── views/           # 页面组件
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── schema.sql           # 数据库 DDL 脚本
└── .gitignore
```

## 快速开始

### 1. 数据库准备

创建 PostgreSQL 数据库并执行 DDL 脚本：

```bash
# 创建数据库
createdb blog_db

# 执行 DDL 脚本
psql -d blog_db -f database/schema.sql
```

### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
# 编辑 .env 文件，修改数据库连接信息

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档: http://localhost:8000/docs

默认管理员账户：
- 用户名: `admin`
- 密码: `admin123`

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问: http://localhost:5173

## 功能特性

### 用户功能
- 用户注册/登录（JWT 认证）
- 文章浏览、搜索、标签筛选
- 文章点赞
- 评论与回复

### 管理功能
- 文章撰写、编辑、删除
- 富文本编辑器集成
- 标签管理
- 评论审核
- 用户管理

## API 接口

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 用户
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新当前用户信息
- `GET /api/users` - 获取用户列表（管理员）

### 文章
- `GET /api/articles` - 获取文章列表（支持分页、搜索、标签筛选）
- `GET /api/articles/{id}` - 获取文章详情
- `POST /api/articles` - 创建文章
- `PUT /api/articles/{id}` - 更新文章
- `DELETE /api/articles/{id}` - 删除文章
- `POST /api/articles/{id}/like` - 点赞文章

### 标签
- `GET /api/tags` - 获取标签列表
- `POST /api/tags` - 创建标签（管理员）
- `PUT /api/tags/{id}` - 更新标签（管理员）
- `DELETE /api/tags/{id}` - 删除标签（管理员）

### 评论
- `GET /api/comments/article/{id}` - 获取文章评论
- `POST /api/comments` - 发表评论
- `GET /api/comments` - 获取所有评论（管理员）
- `PUT /api/comments/{id}/approve` - 审核评论（管理员）
- `DELETE /api/comments/{id}` - 删除评论

## 许可证

MIT License
