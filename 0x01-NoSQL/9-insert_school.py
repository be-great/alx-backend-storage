#!/usr/bin/env python3
"""insert a document in python"""


def insert_school(mongo_collection, **kwargs):
    """insert a document in python"""
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
