# Bilibili Clone

这是一个模仿B站（哔哩哔哩）界面的前端页面，具有响应式设计和基本的交互功能。

## 功能特点

- 完整的B站风格界面设计
- 响应式布局，适配不同屏幕尺寸
- 导航栏、搜索功能、视频卡片布局
- 模拟轮播图自动切换
- 悬停动画效果
- 搜索功能
- 页面滚动头部效果

## 文件结构

```
bilibili-clone/
├── index.html      # 主页面
├── styles.css      # 样式文件
├── script.js       # JavaScript交互功能
└── README.md       # 说明文档
```

## 使用方法

1. 直接在浏览器中打开 `index.html` 文件
2. 或者使用本地服务器运行（推荐）：
   ```bash
   cd bilibili-clone
   python -m http.server 8000
   ```
   然后访问 http://localhost:8000

## 设计说明

- 使用CSS Grid布局实现视频卡片网格
- 使用Flexbox布局实现导航栏和页眉页脚
- 使用媒体查询实现响应式设计
- 使用JavaScript实现页面交互功能

## 浏览器兼容性

- Chrome
- Firefox
- Safari
- Edge

## 注意事项

- 此项目仅供学习和演示使用
- 所有图片均使用占位图服务
- 实际项目中需要替换为真实的API和数据