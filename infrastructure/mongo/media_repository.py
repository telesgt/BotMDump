import json

from config.mongo_config import MongoConfig
from model.mongo.media import Media

class MediaRepository:

	def __init__(self) -> None:
		self.client = MongoConfig.get_connection()

	
	def insert_media(self, media : Media):
		
		try:			

			db = self.client.GachaWaifu
			collection = db.media

			media_dict = json.loads(json.dumps(media, default=lambda o: o.__dict__))
			
			inserted_result = collection.insert_one(media_dict)	

			return str(inserted_result.inserted_id)

		except Exception as e:
			print(e)

	def find_media_by_romaji(self, romaji : str):

		try:			

			db = self.client.GachaWaifu
			collection = db.media

			for data in collection.find(filter={"title.romaji":romaji}).limit(1):
				return data

		except Exception as e:
			print(e)

		return None


	def delete_all(self):
		
		try:			

			print('Limpando collection midia')

			db = self.client.GachaWaifu
			collection = db.media

			collection.delete_many({})

		except Exception as e:
			print(e)
	
	def __del__(self):
		self.client.close()