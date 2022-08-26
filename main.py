import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from utils import load_users, load_orders, load_offers, add_users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.Integer)


class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Offers(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.drop_all()
db.create_all()

user = [Users(**row) for row in load_users()]
order = [Orders(**row) for row in load_orders()]
offer = [Offers(**row) for row in load_offers()]

db.session.add_all(user)
db.session.add_all(order)
db.session.add_all(offer)

db.session.commit()


@app.route('/users/', methods=['GET', 'POST'])
def users_page():

    ###    МЕТОД GET   ###

    users = Users.query.all()

    result = []
    for user in users:
        result.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
             }
        )

    ###    МЕТОД POST   ###
    if request.method == 'POST':
        new_post = request.json
        result.append(new_post)
        add_users(result)
    return json.dumps(result)


@app.route('/users/<int:id>',  methods=['GET', 'DELETE', 'PUT'])
def user_page(id: int):

    ###   МЕТОД PUT   ###

    if request.method == 'PUT':
        new_post = request.json

        users = Users.query.all()

        result = []
        for user in users:
            if id == user.id:
                result.append(
                    {
                        "id": new_post['id'],
                        "first_name": new_post['first_name'],
                        "last_name": new_post['last_name'],
                        "age": new_post['age'],
                        "email": new_post['email'],
                        "role": new_post['role'],
                        "phone": new_post['phone']
                    }
                )
            else:
                result.append(
                    {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "age": user.age,
                        "email": user.email,
                        "role": user.role,
                        "phone": user.phone
                    }
                )
            add_users(result)
        return json.dumps(result)

    ###   МЕТОД DELETE   ###

    if request.method == 'DELETE':

        users = Users.query.all()

        result = []
        for user in users:
            if id != user.id:
                result.append(
                    {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "age": user.age,
                        "email": user.email,
                        "role": user.role,
                        "phone": user.phone
                    }
                )
            add_users(result)
        return json.dumps(result)

    ###    МЕТОД GET    ###

    user = Users.query.get(id)

    if user is None:
        return "This user was not found"

    return json.dumps(
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }
    )


@app.get('/orders/')
def orders_page():
    orders = Orders.query.all()

    result = []
    for order in orders:
        result.append(
            {
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id
             }
        )
    return json.dumps(result, ensure_ascii=False)


@app.get('/orders/<int:id>')
def order_page(id: int):
    order = Orders.query.get(id)
    if order is None:
        return "This order was not found"

    return json.dumps(
        {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        },
        ensure_ascii=False
    )


@app.get('/offers/')
def offers_page():
    offers = Offers.query.all()

    result = []
    for offer in offers:
        result.append(
            {
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id
             }
        )
    return json.dumps(result)


@app.get('/offers/<int:id>')
def offer_page(id: int):
    offer = Offers.query.get(id)
    if offer is None:
        return "This offer was not found"

    return json.dumps(
        {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
