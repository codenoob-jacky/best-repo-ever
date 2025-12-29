# Bilibili Clone

这是一个使用Django开发的仿Bilibili视频分享网站。

## 项目特性

- 用户注册和登录系统
- 视频上传和管理
- 视频分类和标签
- 评论和回复系统
- 点赞/踩功能
- 用户个人主页
- 视频浏览统计

## 技术栈

- Django 6.0
- Python 3
- SQLite (默认数据库)
- Bootstrap 5 (前端框架)
- jQuery

## 快速开始

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install Django
   ```
3. 进入项目目录并运行迁移：
   ```bash
   python manage.py migrate
   ```
4. 创建超级用户：
   ```bash
   python manage.py createsuperuser
   ```
5. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```
6. 访问 `http://127.0.0.1:8000/` 查看网站

## 应用结构

- `videos`: 视频管理相关功能
- `users`: 用户管理相关功能
- `comments`: 评论系统
- `bilibili_clone`: 项目配置

## 管理后台

访问 `http://127.0.0.1:8000/admin/` 进入管理后台，使用创建的超级用户账号登录。

## 功能说明

- 用户可以上传视频
- 用户可以观看、点赞/踩视频
- 用户可以对视频进行评论
- 用户可以关注其他用户
- 视频分类和标签管理
- 个人资料编辑

## 项目结构

```
bilibili_clone/          # 项目根目录
├── bilibili_clone/      # 项目配置
│   ├── __init__.py
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主URL配置
│   ├── wsgi.py
│   └── asgi.py
├── videos/              # 视频应用
│   ├── models.py        # 视频相关模型
│   ├── views.py         # 视频相关视图
│   ├── urls.py          # 视频相关URL
│   └── ...
├── users/               # 用户应用
├── comments/            # 评论应用
├── templates/           # 模板文件
├── static/              # 静态文件
├── media/               # 媒体文件（上传的视频、图片等）
├── manage.py            # Django管理脚本
└── README.md
```

## 待完善功能

- 视频播放器集成
- 更完善的用户系统
- 消息通知系统
- 弹幕功能
- 视频推荐算法
- 更好的前端交互体验