from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

class Item(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50), nullable=True)

    def __repr__(self):
        return self.name
