import pymongo
import pandas as pd

def machine_data():
    client = pymongo.MongoClient("mongodb://admin:freudenberg@localhost:27017/")
    
    db = client['injections']
    collection = db['injections']
    cursor = collection.find()
    machine_data_list = list(cursor)
    
    formatted_data = {
    "machine": [d.get("machine_id") for d in machine_data_list],
    "type": [d.get("result").get("type") for d in machine_data_list],
    "capacity_per_hour": [d.get("result").get("capacity_per_hour") for d in machine_data_list],
    "change_product_A": [d.get("result").get("change_product_A", None) for d in machine_data_list],
    "change_product_B": [d.get("result").get("change_product_B", None) for d in machine_data_list],
    }
    
    return formatted_data
    