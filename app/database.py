from pymongo import mongo_client
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('MongoDB Connected Successfully...')

db = client[settings.MONGO_INITDB_DATABASE]

OurAssistant = db.Assistant
AssistantThreads = db.AssistantThreads