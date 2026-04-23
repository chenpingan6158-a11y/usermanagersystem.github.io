# 用户管理系统

## 项目简介

一个基于 Flask + Vue 3 + MySQL 的前后端分离用户管理系统，支持用户登录注册、信息管理、数据统计等功能。

## 技术栈

- **后端**：Flask、Flask-SQLAlchemy、Flask-CORS、python-dotenv
- **前端**：Vue 3、Axios、Chart.js
- **数据库**：MySQL

## 本地运行方式

1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `.env` 文件中的数据库连接信息
3. 在MySQL中创建数据库：`CREATE DATABASE flask_vue_db;`
4. 启动应用：`python app.py`
5. 访问：`http://127.0.0.1:5000`

## 运行截图

运行截图存放于 `screenshot` 文件夹中，包括：
- 登录页面
- 首页（数据可视化）
- 添加用户页面
- 用户列表页面
- 统计页面