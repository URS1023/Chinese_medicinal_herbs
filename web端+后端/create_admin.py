from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # 检查是否已存在管理员账号
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            print(f"已存在管理员账号: {admin.username}")
            return
        
        # 创建新的管理员账号
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("管理员账号创建成功！")
        print("用户名: admin")
        print("密码: admin123")

if __name__ == "__main__":
    create_admin() 