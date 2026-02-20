from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URL) # initialize a connection to the mongodb server
db = client["inventory_db"] # select a spesfic database in the collection if not ther it will create with that name 
inventory_collection = db["inventory"] # integreate with the collectoin     