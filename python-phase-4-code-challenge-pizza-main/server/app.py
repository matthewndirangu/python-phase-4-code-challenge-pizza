#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route("/restaurants")
def get_restaurants():
    restaurants_dict = [r.to_dict(only = ('id', 'name', 'address')) for r in Restaurant.query.all()]

    response = make_response(restaurants_dict, 200)

    return response


@app.route("/restaurants/<int:restaurant_id>")
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    restaurant_dict = restaurant.to_dict()

    response = make_response(restaurant_dict, 200)

    return response

@app.route("/restaurants/<int:restaurant_id>", methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()

    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)
    
    db.session.delete(restaurant)
    db.session.commit()
    response = make_response("", 204)
    return response

@app.route("/pizzas")
def get_pizzas():
    pizzas_dict = [p.to_dict(only = ('id', 'name', 'ingredients')) for p in Pizza.query.all()]

    response = make_response(pizzas_dict, 200)

    return response


@app.route("/restaurant_pizzas", methods=["POST"])
def post_restaurant_pizzas():
    data = request.get_json()

    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not 1 <= price <=30 or not pizza_id or not restaurant_id:
        return make_response({"errors": ["validation errors"]}, 400)
    
    session = db.session()
    
    pizza = session.get(Pizza, pizza_id)
    restaurant = session.get(Restaurant, restaurant_id)
    
    if not pizza or not restaurant:
        return make_response({"errors": ["validation errors"]}, 404)
    
    restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
   

    db.session.add(restaurant_pizza)
    db.session.commit()

    response = make_response(restaurant_pizza.to_dict(), 201)
    return response





    
   



   




if __name__ == "__main__":
    app.run(port=5555, debug=True)
