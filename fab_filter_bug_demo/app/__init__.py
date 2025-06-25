from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from .views import ItemApi

app = Flask(__name__)
app.config.from_object('config')

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

appbuilder.add_api(ItemApi)
