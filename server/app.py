from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return '<h1>Bakery API</h1>'


# GET /bakeries
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])


# GET /bakeries/<int:id>
@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict(nested=True))


# GET /baked_goods/by_price
@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([bg.to_dict() for bg in baked_goods])


# GET /baked_goods/most_expensive
@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.to_dict())
