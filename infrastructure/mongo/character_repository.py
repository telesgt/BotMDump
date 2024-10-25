import json

from config.mongo_config import MongoConfig
from model.mongo.character import Character

class CharacterRepository:

	def __init__(self) -> None:
		self.client = MongoConfig.get_connection()

	
	def insert_waifu(self, character : Character):
		
		try:			

			db = self.client.GachaWaifu
			collection = db.characters

			character_dict = json.loads(json.dumps(character, default=lambda o: o.__dict__))
			
			collection.insert_one(character_dict)			

		except Exception as e:
			print(e)

	def delete_all(self):
		
		try:			

			db = self.client.GachaWaifu
			collection = db.characters

			collection.delete_many({})

		except Exception as e:
			print(e)
	
	def __del__(self):
		self.client.close()