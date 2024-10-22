#!/usr/bin/env python3
"""12. Log stats"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """change school topics"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


def run():
    "prime code"
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print('{} logs'.format(collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = len(list(collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, count))
    # count get=> /status path
    count_get_status = len(list(
        collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(count_get_status))


if __name__ == '__main__':
    run()
