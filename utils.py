import json


def load_users():
    with open('users.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def add_users(filename):
    with open('users.json', 'w', encoding='utf-8') as file:
        return json.dump(filename, file)


def load_orders():
    with open('orders.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def load_offers():
    with open('offers.json', 'r', encoding='utf-8') as file:
        return json.load(file)
