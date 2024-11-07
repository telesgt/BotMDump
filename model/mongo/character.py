from typing import List

from model.mongo.character_images import CharacterImages

class Character:

	def __init__(self):		
		self.images = CharacterImages()
		self.name = None
		self.name_kanji = None
		self.nicknames : List[str] = []
		self.rarity = None
		self.gender = None
		self.media_id : List[str] = []