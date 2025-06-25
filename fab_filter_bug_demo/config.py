import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
FAB_API_SWAGGER_UI = True
SECRET_KEY = "this-is-a-secret-key-for-testing"  # 生产环境请换成更安全的随机字符串
