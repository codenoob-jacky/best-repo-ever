# 仿Bilibili网站数据库模型文档

## 概述
本项目是一个仿Bilibili视频网站，包含视频管理、用户系统、评论系统等核心功能。数据库设计遵循关系型数据库设计原则，使用Django ORM实现。

## 数据库模型

### 1. 用户系统 (users app)

#### 1.1 UserProfile 模型
- **user**: OneToOneField - 关联Django内置User模型
- **bio**: TextField - 用户简介 (最大500字符，可选)
- **location**: CharField - 位置 (最大30字符，可选)
- **birth_date**: DateField - 出生日期 (可选)
- **avatar**: ImageField - 头像 (可选)
- **followers**: ManyToManyField - 关注者 (关联User模型，related_name='following')
- **following**: ManyToManyField - 关注的用户 (关联User模型，related_name='followers')
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **updated_at**: DateTimeField - 更新时间 (自动更新)
- **verified**: BooleanField - 认证标识 (默认False)
- **total_videos**: PositiveIntegerField - 总视频数 (默认0)
- **total_views**: PositiveIntegerField - 总观看数 (默认0)
- **total_likes**: PositiveIntegerField - 总点赞数 (默认0)

#### 1.2 UserFollow 模型
- **follower**: ForeignKey - 关注者 (关联User，related_name='following_relations')
- **followed**: ForeignKey - 被关注者 (关联User，related_name='follower_relations')
- **created_at**: DateTimeField - 关注时间 (自动添加)
- **Meta.unique_together**: ('follower', 'followed') - 确保唯一关注关系

### 2. 视频系统 (videos app)

#### 2.1 Video 模型
- **title**: CharField - 视频标题 (最大200字符)
- **description**: TextField - 视频描述
- **video_file**: FileField - 视频文件 (上传到videos/目录)
- **thumbnail**: ImageField - 缩略图 (上传到thumbnails/目录，可选)
- **uploader**: ForeignKey - 上传者 (关联User，related_name='uploaded_videos')
- **upload_date**: DateTimeField - 上传时间 (自动添加)
- **views**: PositiveIntegerField - 观看次数 (默认0) - 已废弃，使用view_count
- **likes**: PositiveIntegerField - 点赞数 (默认0) - 已废弃，使用like_count
- **dislikes**: PositiveIntegerField - 点踩数 (默认0) - 已废弃，使用dislike_count
- **duration**: DurationField - 视频时长 (可选)
- **published**: BooleanField - 是否发布 (默认True)
- **view_count**: PositiveIntegerField - 观看次数 (默认0)
- **like_count**: PositiveIntegerField - 点赞数 (默认0)
- **dislike_count**: PositiveIntegerField - 点踩数 (默认0)
- **comment_count**: PositiveIntegerField - 评论数 (默认0)

#### 2.2 VideoCategory 模型
- **name**: CharField - 分类名称 (最大100字符)
- **description**: TextField - 分类描述 (可选)

#### 2.3 VideoTag 模型
- **name**: CharField - 标签名称 (最大50字符)

#### 2.4 VideoCategoryRelation 模型
- **video**: ForeignKey - 关联视频
- **category**: ForeignKey - 关联分类
- **Meta.unique_together**: ('video', 'category') - 确保视频与分类的唯一关系

#### 2.5 VideoTagRelation 模型
- **video**: ForeignKey - 关联视频
- **tag**: ForeignKey - 关联标签
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **Meta.unique_together**: ('video', 'tag') - 确保视频与标签的唯一关系

#### 2.6 VideoReaction 模型 (视频点赞/点踩)
- **video**: ForeignKey - 关联视频 (related_name='video_reactions')
- **user**: ForeignKey - 关联用户
- **reaction_type**: CharField - 反应类型 ('like'或'dislike')
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **Meta.unique_together**: ('video', 'user') - 确保用户对视频的唯一反应

#### 2.7 VideoView 模型 (视频观看记录)
- **video**: ForeignKey - 关联视频 (related_name='video_views')
- **user**: ForeignKey - 关联用户 (可选)
- **ip_address**: GenericIPAddressField - IP地址 (可选)
- **viewed_at**: DateTimeField - 观看时间 (自动添加)
- **session_key**: CharField - 会话密钥 (最大40字符，可选)
- **Meta.unique_together**: ('video', 'user', 'session_key', 'ip_address') - 防止重复计数

#### 2.8 Playlist 模型 (播放列表)
- **name**: CharField - 播放列表名称 (最大200字符)
- **description**: TextField - 描述 (可选)
- **owner**: ForeignKey - 所有者 (关联User，related_name='playlists')
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **updated_at**: DateTimeField - 更新时间 (自动更新)
- **is_public**: BooleanField - 是否公开 (默认True)

#### 2.9 PlaylistItem 模型 (播放列表项目)
- **playlist**: ForeignKey - 关联播放列表 (related_name='items')
- **video**: ForeignKey - 关联视频
- **added_at**: DateTimeField - 添加时间 (自动添加)
- **position**: PositiveIntegerField - 位置序号
- **Meta.unique_together**: ('playlist', 'position') - 确保播放列表中位置的唯一性
- **Meta.ordering**: ['position'] - 按位置排序

### 3. 评论系统 (comments app)

#### 3.1 Comment 模型
- **video**: ForeignKey - 关联视频 (related_name='comments')
- **author**: ForeignKey - 作者 (关联User)
- **content**: TextField - 评论内容
- **parent**: ForeignKey - 父评论 (自关联，可选，related_name='replies')
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **updated_at**: DateTimeField - 更新时间 (自动更新)
- **likes**: PositiveIntegerField - 点赞数 (默认0)
- **dislikes**: PositiveIntegerField - 点踩数 (默认0)
- **is_edited**: BooleanField - 是否被编辑过 (默认False)
- **is_deleted**: BooleanField - 是否被删除 (默认False)
- **Meta.ordering**: ['created_at'] - 按创建时间排序

#### 3.2 CommentReaction 模型 (评论点赞/点踩)
- **comment**: ForeignKey - 关联评论 (related_name='comment_reactions')
- **user**: ForeignKey - 关联用户
- **reaction_type**: CharField - 反应类型 ('like'或'dislike')
- **created_at**: DateTimeField - 创建时间 (自动添加)
- **Meta.unique_together**: ('comment', 'user') - 确保用户对评论的唯一反应

## 关系图
```
User --1:1--> UserProfile
User --M:M--> User (through UserFollow)
User --1:M--> Video (as uploader)
User --1:M--> Comment (as author)
User --1:M--> VideoReaction
User --1:M--> CommentReaction
User --1:M--> VideoView

Video --1:M--> Comment
Video --1:M--> VideoReaction
Video --1:M--> VideoView
Video --1:M--> PlaylistItem
Video --M:M--> VideoCategory (through VideoCategoryRelation)
Video --M:M--> VideoTag (through VideoTagRelation)

Comment --1:M--> Comment (replies)
Comment --1:M--> CommentReaction

Playlist --1:M--> PlaylistItem
```

## 特殊属性和方法

### Video模型
- `total_likes` property: 获取视频总点赞数
- `total_dislikes` property: 获取视频总点踩数
- Meta.ordering: 按上传时间倒序排列

### Comment模型
- `total_likes` property: 获取评论总点赞数
- `total_dislikes` property: 获取评论总点踩数
- Meta.ordering: 按创建时间升序排列

### UserProfile模型
- `follower_count` property: 获取关注者数量
- `following_count` property: 获取关注数量
- `video_count` property: 获取上传视频数量

## 数据库索引和优化
- 视频按上传时间排序
- 评论按创建时间排序
- 用户关注关系唯一性约束
- 视频与分类、标签的唯一性约束
- 观看记录防重复机制

## 扩展性考虑
- 使用related_name便于反向查询
- 支持软删除（is_deleted字段）
- 支持分级评论（parent字段）
- 支持视频分类和标签系统
- 支持播放列表功能
- 支持用户认证系统