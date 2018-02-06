import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.chatbot

USERS_COLLECTION = db.users
MESSAGE_COLLECTION = db.messages
