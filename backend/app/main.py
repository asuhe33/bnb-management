from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import auth, rooms, bookings, dashboard

app = FastAPI(
    title="民宿管理系统 API",
    description="前后端分离的民宿管理后端 - FastAPI + MySQL + JWT",
    version="1.0.0",
)

# CORS 开发期全部放开，生产环境应限制来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["根路径"])
def root():
    return {"message": "民宿管理系统 API", "docs": "/docs"}
