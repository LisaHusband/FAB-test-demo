from app import app, db
from app.models import Item

from app import app, db
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.sqla.models import Role



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # 1. 清空旧数据
        db.session.query(Item).delete()
        db.session.commit()
        print("Old Item data cleared.")

        # 2. 插入新的测试数据
        categories = ['Test', 'Demo', 'Other', 'CategoryA', 'CategoryB']
        for cat in categories:
            for i in range(500):  # 每类 5 条记录
                db.session.add(Item(name=f"{cat}_Item_{i}", category=cat))
        db.session.commit()
        print("Test data inserted.")

        # 3. 创建 admin 账户（如果不存在）
        sm = app.appbuilder.sm
        if not sm.find_user(username="admin"):
            admin_role = sm.find_role("Admin")
            sm.add_user(
                username="admin",
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                role=admin_role,
                password="admin"
            )
            print("Admin user created.")
        else:
            print("Admin user already exists.")

    app.run(debug=True, threaded=True, port=5000)
