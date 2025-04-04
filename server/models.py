from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()


class Bakery(db.Model):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    baked_goods = db.relationship('BakedGood', backref='bakery')

    def to_dict(self, nested=False):
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }
        if nested:
            data["baked_goods"] = [bg.to_dict() for bg in self.baked_goods]
        return data


class BakedGood(db.Model):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "bakery_id": self.bakery_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "bakery": self.bakery.to_dict() if self.bakery else None
        }
