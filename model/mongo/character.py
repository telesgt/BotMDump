from typing import List

from model.mongo.character_images import CharacterImages

class Character:

	def __init__(self):		
		self.images = None
		self.name = None
		self.name_kanji = None
		self.nicknames = []
		self.favorites = None