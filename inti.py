import os

project_files = {
    "fab_filter_bug_demo/requirements.txt": """Flask==2.3.3
Flask-AppBuilder==4.3.0
""",
    "fab_filter_bug_demo/config.py": """import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
FAB_API_SWAGGER_UI = True
""",
    "fab_filter_bug_demo/app/__init__.py": """from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from .views import ItemApi

app = Flask(__name__)
app.config.from_object('config')

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

appbuilder.add_api(ItemApi)
""",
    "fab_filter_bug_demo/app/models.py": """from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

class Item(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50), nullable=True)

    def __repr__(self):
        return self.name
""",
    "fab_filter_bug_demo/app/views.py": """from flask_appbuilder import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Item

class ItemApi(ModelRestApi):
    resource_name = 'item'
    datamodel = SQLAInterface(Item)
    allow_browser_login = True
    list_columns = ['id', 'name', 'category']
    show_columns = ['id', 'name', 'category']
""",
    "fab_filter_bug_demo/run.py": """from app import app, db
from app.models import Item

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Item.query.first():
            for i in range(5):
                db.session.add(Item(name=f"Item {i}", category="Test"))
            db.session.commit()

    app.run(debug=True, threaded=True, port=5000)
""",
    "fab_filter_bug_demo/stress_test.py": """import requests
import threading

def query(i):
    r = requests.get("http://127.0.0.1:5000/api/v1/item/?q=(filters:!((col:category,opr:eq,value:'Test')))")
    print(f"Thread {i} - Response length: {len(r.text)}")

threads = []

for i in range(20):
    t = threading.Thread(target=query, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
"""
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

for filepath, content in project_files.items():
    dirpath = os.path.dirname(filepath)
    ensure_dir(dirpath)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Flask App Builder filter bug demo project has been generated.")
