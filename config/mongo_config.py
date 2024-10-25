import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoConfig:

	URI = os.environ['DB_URI']
		
	@staticmethod
	def get_connection():
		cli = MongoClient(MongoConfig.URI, server_api=ServerApi('1'))
		return cli