-- ============================================================================
-- 个人博客内容管理系统 - PostgreSQL 数据库 DDL 脚本
-- 描述: 定义博客系统的核心表结构，包含用户、文章、标签、评论等实体
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 删除已存在的表（按依赖关系顺序，方便重新初始化）
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS article_tags CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================================
-- 1. 用户表 (users)
-- ============================================================================
-- 存储系统用户信息，支持JWT登录认证
-- ============================================================================
CREATE TABLE users (
    id              SERIAL          PRIMARY KEY,                    -- 用户主键ID，自增
    username        VARCHAR(50)     NOT NULL UNIQUE,                -- 用户名，唯一，用于登录
    email           VARCHAR(255)    NOT NULL UNIQUE,                -- 邮箱，唯一，用于通知
    password_hash   VARCHAR(255)    NOT NULL,                       -- 密码哈希值（bcrypt加密）
    avatar_url      VARCHAR(512),                                   -- 用户头像URL，可选
    bio             TEXT,                                           -- 用户简介/个人说明
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,          -- 账户是否激活
    is_admin        BOOLEAN         NOT NULL DEFAULT FALSE,         -- 是否为管理员
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),         -- 创建时间
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()          -- 更新时间
);

-- 为常用查询字段添加索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- 2. 文章表 (articles)
-- ============================================================================
-- 存储博客文章内容，支持富文本、标签关联、浏览计数
-- ============================================================================
CREATE TABLE articles (
    id              SERIAL          PRIMARY KEY,                    -- 文章主键ID，自增
    title           VARCHAR(500)    NOT NULL,                       -- 文章标题
    slug            VARCHAR(500)    NOT NULL UNIQUE,                -- 文章URL友好的slug标识
    summary         VARCHAR(1000),                                  -- 文章摘要/简短描述
    content         TEXT            NOT NULL,                       -- 文章正文内容（富文本HTML）
    cover_image     VARCHAR(512),                                   -- 封面图片URL
    author_id       INTEGER         NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- 作者ID，外键关联用户表
    views_count     INTEGER         NOT NULL DEFAULT 0,             -- 浏览次数统计
    likes_count     INTEGER         NOT NULL DEFAULT 0,             -- 点赞次数统计
    is_published    BOOLEAN         NOT NULL DEFAULT TRUE,          -- 是否发布（草稿vs已发布）
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),         -- 创建时间
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()          -- 更新时间
);

-- 为常用查询字段添加索引
CREATE INDEX idx_articles_author_id ON articles(author_id);
CREATE INDEX idx_articles_is_published ON articles(is_published);
CREATE INDEX idx_articles_created_at ON articles(created_at DESC);
CREATE INDEX idx_articles_slug ON articles(slug);

-- ============================================================================
-- 3. 标签表 (tags)
-- ============================================================================
-- 存储文章标签，用于分类和筛选文章
-- ============================================================================
CREATE TABLE tags (
    id              SERIAL          PRIMARY KEY,                    -- 标签主键ID，自增
    name            VARCHAR(100)    NOT NULL UNIQUE,                -- 标签名称，唯一
    slug            VARCHAR(100)    NOT NULL UNIQUE,                -- 标签URL友好的slug标识
    description     VARCHAR(500),                                   -- 标签描述，可选
    color           VARCHAR(20)     DEFAULT '#1890ff',              -- 标签显示颜色
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()          -- 创建时间
);

-- 为标签名添加索引
CREATE INDEX idx_tags_name ON tags(name);

-- ============================================================================
-- 4. 文章-标签关联表 (article_tags)
-- ============================================================================
-- 多对多关系表：一篇文章可以有多个标签，一个标签可以关联多篇文章
-- ============================================================================
CREATE TABLE article_tags (
    article_id      INTEGER         NOT NULL REFERENCES articles(id) ON DELETE CASCADE,  -- 文章ID，外键
    tag_id          INTEGER         NOT NULL REFERENCES tags(id) ON DELETE CASCADE,      -- 标签ID，外键
    PRIMARY KEY (article_id, tag_id)                                                     -- 复合主键，防止重复关联
);

-- 为关联查询添加索引
CREATE INDEX idx_article_tags_tag_id ON article_tags(tag_id);
CREATE INDEX idx_article_tags_article_id ON article_tags(article_id);

-- ============================================================================
-- 5. 评论表 (comments)
-- ============================================================================
-- 存储文章评论，支持嵌套回复（通过parent_id实现树形结构）
-- ============================================================================
CREATE TABLE comments (
    id              SERIAL          PRIMARY KEY,                    -- 评论主键ID，自增
    article_id      INTEGER         NOT NULL REFERENCES articles(id) ON DELETE CASCADE,  -- 所属文章ID
    user_id         INTEGER         NOT NULL REFERENCES users(id) ON DELETE CASCADE,     -- 评论用户ID
    parent_id       INTEGER         REFERENCES comments(id) ON DELETE CASCADE,           -- 父评论ID，NULL表示顶级评论
    content         TEXT            NOT NULL,                       -- 评论内容
    is_approved     BOOLEAN         NOT NULL DEFAULT TRUE,          -- 是否已审核通过（管理员可审核）
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),         -- 创建时间
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()          -- 更新时间
);

-- 为常用查询字段添加索引
CREATE INDEX idx_comments_article_id ON comments(article_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);
CREATE INDEX idx_comments_is_approved ON comments(is_approved);
CREATE INDEX idx_comments_created_at ON comments(created_at);

-- ============================================================================
-- 自动更新时间戳的触发器函数
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为需要自动更新updated_at的表创建触发器
CREATE TRIGGER trigger_update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_update_articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_update_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 初始数据：创建默认管理员账户
-- 密码: admin123 (使用bcrypt加密)
-- 注意：如需重置密码，请运行后端提供的脚本或修改此SQL中的密码哈希
-- ============================================================================
INSERT INTO users (username, email, password_hash, is_admin, bio)
VALUES (
    'admin',
    'admin@blog.com',
    '$2b$12$jCyY8rBK5hMgnSRxBsZQAe.efGfCJz9mcmj1fnNAHrevrFfdsol26',
    TRUE,
    '系统管理员'
);

-- ============================================================================
-- 初始数据：创建一些示例标签
-- ============================================================================
INSERT INTO tags (name, slug, description, color) VALUES
    ('技术', 'tech', '技术相关文章', '#1890ff'),
    ('生活', 'life', '生活随笔', '#52c41a'),
    ('教程', 'tutorial', '教程类文章', '#722ed1'),
    ('原创', 'original', '原创内容', '#fa8c16'),
    ('随笔', 'notes', '随笔记录', '#eb2f96');
