import os
import logging
import json
from json import JSONEncoder

from infrastructure.jikan.character_api import CharacterApi
from infrastructure.mongo.character_repository import CharacterRepository
from model.jikan.character_search_request import CharacterSearchRequest
from model.mongo.character import Character
from model.mongo.character_images import CharacterImages
from model.mongo.image import Image

class CharacterDump():

	def __init__(self) -> None:
		self.character_repository = CharacterRepository()
	
	def doDump(self):

		character_api = CharacterApi()

		character_request = CharacterSearchRequest()		
		character_request.page = 1
		character_request.order_by = "favorites"
		character_request.sort = "desc"

		jikan_response = character_api.search(character_request)

		for character in jikan_response['data']:
			
			mongo_character = self.create_mongo_character(character)

			self.character_repository.insert_waifu(mongo_character)

	def create_mongo_character(self, character_dict) -> Character:

		image = Image()
		image.image_url = character_dict['images']['jpg']['image_url']		

		character_images = CharacterImages()
		character_images.jpg = image
		
		character = Character()
		character.images = character_images
		character.name = character_dict['name']
		character.name_kanji = character_dict['name_kanji']
		character.nicknames = character_dict['nicknames']
		character.favorites = character_dict['favorites']

		return character

