from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoConfig:

	URI = "mongodb://root:example@127.0.0.1"		
		
	@staticmethod
	def openConnection():
		cli = MongoClient(MongoConfig.URI, server_api=ServerApi('1'))
		return cli
	
	def __setattr__(self, name, value):
		raise TypeError("Constants are immutable")