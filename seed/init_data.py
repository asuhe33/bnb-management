"""
种子数据初始化脚本
运行方式: python seed/init_data.py
"""
import sys
import os
from datetime import date, timedelta

# 将 backend 目录加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import SessionLocal, init_db
from app.models import User, Room, Booking
from app.utils.security import hash_password


def seed():
    init_db()
    db = SessionLocal()
    try:
        # 清空旧数据（开发用）
        db.query(Booking).delete()
        db.query(Room).delete()
        db.query(User).delete()
        db.commit()

        # 创建管理员用户
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            full_name="管理员",
            role="admin",
        )
        db.add(admin)
        db.commit()
        print("✓ 创建用户: admin / admin123")

        # 创建示例房源
        rooms_data = [
            {
                "name": "山景小屋",
                "type": "whole",
                "price": 680,
                "capacity": 6,
                "amenities": ["WiFi", "空调", "厨房", "山景阳台", "停车位"],
                "description": "独栋木屋，坐拥山谷全景，适合家庭度假",
                "image_url": "",
            },
            {
                "name": "竹林雅居",
                "type": "suite",
                "price": 380,
                "capacity": 3,
                "amenities": ["WiFi", "空调", "独立卫浴", "竹林景观"],
                "description": "被竹林环绕的雅致套房，静谧私密",
                "image_url": "",
            },
            {
                "name": "听涛阁",
                "type": "suite",
                "price": 420,
                "capacity": 2,
                "amenities": ["WiFi", "空调", "海景阳台", "浴缸"],
                "description": "推窗即是大海，枕着涛声入眠",
                "image_url": "",
            },
            {
                "name": "暖阳单间 A",
                "type": "single",
                "price": 180,
                "capacity": 2,
                "amenities": ["WiFi", "空调", "独立卫浴"],
                "description": "温馨单人房，阳光充足，性价比之选",
                "image_url": "",
            },
            {
                "name": "暖阳单间 B",
                "type": "single",
                "price": 180,
                "capacity": 2,
                "amenities": ["WiFi", "空调", "独立卫浴"],
                "description": "温馨单人房，阳光充足，性价比之选",
                "image_url": "",
            },
            {
                "name": "星空阁楼",
                "type": "suite",
                "price": 520,
                "capacity": 4,
                "amenities": ["WiFi", "空调", "天窗观星", "投影仪", "露台"],
                "description": "顶层阁楼，夜晚可观星空，浪漫满分",
                "image_url": "",
            },
        ]

        room_objs = []
        for r in rooms_data:
            room = Room(**r)
            db.add(room)
            room_objs.append(room)
        db.commit()
        print(f"✓ 创建 {len(room_objs)} 个房源")

        # 创建示例预订
        today = date.today()
        bookings_data = [
            (room_objs[0], "张先生", "13800138001", today - timedelta(days=10), today - timedelta(days=7), "confirmed"),
            (room_objs[1], "李女士", "13800138002", today - timedelta(days=5), today - timedelta(days=2), "checked_out"),
            (room_objs[2], "王先生", "13800138003", today - timedelta(days=3), today, "checked_in"),
            (room_objs[3], "赵女士", "13800138004", today - timedelta(days=2), today + timedelta(days=1), "confirmed"),
            (room_objs[4], "陈先生", "13800138005", today + timedelta(days=1), today + timedelta(days=3), "pending"),
            (room_objs[5], "刘女士", "13800138006", today - timedelta(days=7), today - timedelta(days=4), "checked_out"),
            (room_objs[0], "周先生", "13800138007", today + timedelta(days=5), today + timedelta(days=8), "pending"),
            (room_objs[1], "吴女士", "13800138008", today - timedelta(days=1), today + timedelta(days=2), "confirmed"),
        ]

        for room, guest, phone, ci, co, status in bookings_data:
            nights = (co - ci).days
            total = float(room.price) * nights
            booking = Booking(
                room_id=room.id,
                user_id=admin.id,
                guest_name=guest,
                guest_phone=phone,
                check_in=ci,
                check_out=co,
                nights=nights,
                total_price=total,
                status=status,
            )
            db.add(booking)
        db.commit()
        print(f"✓ 创建 {len(bookings_data)} 条预订")

        print("\n🎉 种子数据初始化完成！")
        print("   登录账号: admin / admin123")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
