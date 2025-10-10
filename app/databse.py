from tinydb import TinyDB, Query
from app.models.product import Product

db = TinyDB('db.json')

def db_put(prod: Product):
    id = 1
    db.insert({
        'id': id,
        'name': prod.name,
        'desc': prod.desc,
        'price': prod.price
    })

def db_get():
    pass

def db_delete_entry():
    pass

def db_clear():
    db.drop_tables()