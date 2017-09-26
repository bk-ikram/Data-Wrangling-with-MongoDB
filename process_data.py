# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 16:06:46 2017

@author: IKRAM
"""

import json
from pymongo import MongoClient

FILENAME = "doha_qatar.osm.json"
    
# open mongodb connection from shell before running this
client = MongoClient("mongodb://localhost:27017")
# create 'osm' database
db = client.osm
# insert each dictionary one by one
# osm.json is not technically JSON but collection of JSONs
def import_json(filename):
    with open(filename, 'r') as fileinput:
        for line in fileinput:
            data = json.loads(line)
            db.doha_qatar.insert_one(data)

def query_db(pipeline):
    result=db.doha_qatar.aggregate(pipeline)
    return result

if __name__ == "__main__":
    #import_json(FILENAME)
    #query_db()
    pass