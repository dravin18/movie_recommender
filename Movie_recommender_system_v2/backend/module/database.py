from pymongo import MongoClient
from . import config
import os
MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

#client = MongoClient(f'mongodb://{config.settings.mongodb_host_name}:{config.settings.mongodb_port}/')
client = MongoClient(f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{config.settings.mongodb_host_name}:{config.settings.mongodb_port}/?authSource=admin')
db = client[config.settings.mongodb_database_name]
movie_collection = db[config.settings.movie_collection_name]
user_collection = db[config.settings.users_collection_name]
rating_collection = db[config.settings.rating_collection_name]