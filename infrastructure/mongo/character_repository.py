import json

from config.mongo_config import MongoConfig
from model.mongo.character import Character

class CharacterRepository:

	def insert_waifu(self, character : Character):
		
		try:			

			client = MongoConfig.openConnection()
			db = client.GachaWaifu
			collection = db.characters

			character_dict = json.loads(json.dumps(character, default=lambda o: o.__dict__))
			
			collection.insert_one(character_dict)			

		except Exception as e:
			print(e)