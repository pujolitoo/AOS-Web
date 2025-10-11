from tinydb import TinyDB, Query
from app.models.product import Product

import json
import os

db = TinyDB('db.json')
id_count = 0

def db_put(prod: Product) -> dict:
    
    global id_count
    
    if len(db_search(prod.name)) > 0: return {}
    
    id = db_get_last_id()
    temp = {
        'id': id,
        'name': prod.name,
        'desc': prod.desc,
        'price': prod.price
    }
    db.insert(temp)
    
    id_count = id_count + 1
    
    return temp

def db_get(id: int) -> Product:
    ocurrences = db.search(Query().id == id)
    if len(ocurrences) < 0: 
        raise Exception(f"Entry with id {id} hasn't been found!")
    found = Product.model_validate(dict(ocurrences[0]), extra='ignore')
    return found

def db_get_last_id():
    return id_count + 1

def db_delete_entry(id: int):
    if id < 0: return
    db.remove(Query().id == id)
    
def db_search(prod_name: str):
    return db.search(Query().name == prod_name)

def db_update(id: int, prod: Product):
    db.update(dict(prod), Query().id == id)
    
def db_remove():
    os.remove("db.json")

def db_clear():
    db.drop_tables()
    id_count = 0