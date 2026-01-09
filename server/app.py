#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries')
def bakeries():
    bakery_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(bakery_list, 200)
    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)

    bakery_dict = bakery.to_dict()
    bakery_dict["baked_goods"] = [bg.to_dict() for bg in bakery.baked_goods]

    return make_response(bakery_dict, 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = (BakedGood.query.order_by(BakedGood.price.desc()).all())

    response = []

    for baked_good in baked_goods:
        baked_good_dict = baked_good.to_dict()

        if baked_good.bakery:
            baked_good_dict["bakery"] = baked_good.bakery.to_dict()
        else:
            baked_good_dict["bakery"] = None

        response.append(baked_good_dict)

    return make_response(response, 200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = (
        BakedGood.query
        .order_by(BakedGood.price.desc())
        .first()
    )

    baked_good_dict = baked_good.to_dict()

    if baked_good.bakery:
        baked_good_dict["bakery"] = baked_good.bakery.to_dict()
    else:
        baked_good_dict["bakery"] = None

    return make_response(baked_good_dict, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
