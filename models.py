from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from CNPM import db, app
from flask_login import UserMixin
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'
    name = Column(String(50), nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='tuyenBay', lazy=True)

    def __str__(self):
        return self.name


class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    tags = relationship('Tag', secondary='tuyenBay_id', lazy='subquery',
                        backref=backref('chuyenbay', lazy=True))

    def __str__(self):
        return self.name

