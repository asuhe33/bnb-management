# 民宿管理系统 (Homestay Manager)

> 前后端分离的全栈 Web 项目 — FastAPI + Flask + MySQL + JWT

一个面向民宿房东的管理平台，覆盖房源管理、预订流程、数据看板等核心业务场景。

## ✨ 功能特性

- **用户认证** — JWT 登录/注册，接口鉴权
- **房源管理** — 房源 CRUD、房型/价格/设施维护、关键词搜索
- **预订管理** — 预订创建、日期冲突检测、状态流转（待确认 → 已确认 → 已入住 → 已退房）
- **数据看板** — 总收益、本月收益、入住率、近 7 日收益趋势、房型占比可视化

## 🏗 技术架构

```
浏览器 → Flask (5000) → FastAPI (8000) → MySQL
         ↓ 静态托管      ↓ REST API
       前端 SPA        JWT 鉴权
```

| 层级 | 技术 |
|------|------|
| 前端 | 原生 HTML / CSS / JS SPA + Chart.js |
| 网关 | Flask（静态托管 + API 反向代理） |
| API | FastAPI（异步 REST + 自动 OpenAPI 文档） |
| 数据库 | MySQL 8.0 + SQLAlchemy ORM |
| 认证 | JWT (python-jose) + bcrypt 密码哈希 |

## 🚀 快速开始

### 1. 环境要求

- Python 3.10+
- MySQL 8.0（或 Docker）

### 2. 启动 MySQL

使用 Docker（推荐）：
```bash
docker-compose up -d
```

或手动创建数据库：
```sql
CREATE DATABASE bnb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 中的数据库连接信息
```

### 4. 安装依赖并启动 FastAPI

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问 Swagger 文档：http://localhost:8000/docs

### 5. 启动 Flask 网关

```bash
cd flask_gateway
pip install -r requirements.txt
python app.py
```

### 6. 初始化示例数据

```bash
python seed/init_data.py
```

默认账号：`admin` / `admin123`

### 7. 访问系统

浏览器打开：**http://localhost:5000**

## 📡 API 接口

启动 FastAPI 后访问 `http://localhost:8000/docs` 查看完整 Swagger 文档。

| 模块 | 接口 | 说明 |
|------|------|------|
| 认证 | `POST /api/auth/register` | 用户注册 |
| 认证 | `POST /api/auth/login` | 用户登录 |
| 认证 | `GET /api/auth/me` | 当前用户信息 |
| 房源 | `GET /api/rooms` | 房源列表（分页/搜索） |
| 房源 | `POST /api/rooms` | 新建房源 |
| 房源 | `PUT /api/rooms/{id}` | 更新房源 |
| 房源 | `DELETE /api/rooms/{id}` | 删除房源 |
| 预订 | `GET /api/bookings` | 预订列表（状态筛选） |
| 预订 | `POST /api/bookings` | 创建预订（含冲突检测） |
| 预订 | `PUT /api/bookings/{id}` | 更新预订状态 |
| 看板 | `GET /api/dashboard/stats` | 聚合统计数据 |

## 📁 项目结构

```
bnb-management/
├── backend/                # FastAPI 后端
│   └── app/
│       ├── main.py         # 应用入口
│       ├── config.py       # 配置管理
│       ├── database.py     # 数据库连接
│       ├── models/         # ORM 模型
│       ├── schemas/        # Pydantic 模型
│       ├── routers/        # 路由层
│       ├── services/       # 业务逻辑
│       └── utils/          # 安全工具
├── flask_gateway/          # Flask 网关
│   ├── app.py              # 静态托管 + 代理
│   └── static/             # 前端资源
├── seed/                   # 种子数据
├── docker-compose.yml      # MySQL 容器
└── .env.example            # 环境变量模板
```

## 🔑 核心业务逻辑

**日期冲突检测** — 创建预订时使用经典区间重叠判断算法：
```python
A.start < B.end AND A.end > B.start
```
冲突时返回 HTTP 409。

**入住率计算** — 近 30 天内已被预订的天数 / (房源数 × 30)。

## 📝 简历描述参考

> **民宿管理系统** | Python / FastAPI / Flask / MySQL / JWT
> - 设计并实现前后端分离的民宿管理平台，FastAPI 提供异步 REST API，Flask 作为前端托管与 API 网关
> - 实现基于 JWT 的用户认证与权限控制，保障接口安全
> - 设计预订日期冲突检测算法（区间重叠判断），自动拦截重复预订
> - 构建数据看板，通过 SQL 聚合查询实现入住率、收益趋势等核心业务指标的可视化
