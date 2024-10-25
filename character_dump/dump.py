import os
import logging
import json
from json import JSONEncoder

from infrastructure.jikan.character_api import CharacterApi as JikanApi
from infrastructure.acdb.character_api import CharacterApi as AcdbApi
from infrastructure.mongo.character_repository import CharacterRepository

from model.jikan.character_search_request import CharacterSearchRequest as JikanRequest
from model.acdb.character_search_request import CharacterSearchRequest as AcdbRequest
from model.mongo.character import Character
from model.mongo.character_images import CharacterImages
from model.mongo.image import Image

class CharacterDump():

	def __init__(self) -> None:
		self.character_repository = CharacterRepository()
		self.jikan_api = JikanApi()
		self.acdb_api = AcdbApi()
	
	def doDump(self, total_personagens):

		print('Limpando collection waifu')

		self.character_repository.delete_all()

		contador_personagens = 0
		page = 0
		raridades = self.calcular_valores_raridade(total_personagens)

		while contador_personagens < total_personagens:

			page += 1

			jikan_request = self.get_request_jikan(page)
			jikan_response = self.jikan_api.search(jikan_request)

			for jikan_character in jikan_response['data']:

				contador_personagens += 1
				
				# acdb_request = self.get_request_acdb(jikan_character['name'])
				# acdb_character = self.acdb_api.find_by_name(acdb_request)

				mongo_character = self.create_mongo_character(jikan_character, raridade=self.get_raridade_personagem(raridades, contador_personagens))
				self.character_repository.insert_waifu(mongo_character)
			
			if jikan_response['pagination']['has_next_page'] == False:
				print('Sem mais personagens para buscar')
				break

			

	def create_mongo_character(self, jikan_character, acdb_character=None, raridade=None) -> Character:

		image = Image()
		image.image_url = jikan_character['images']['jpg']['image_url']
		image.small_image_url = jikan_character['images']['jpg'].get('small_image_url')

		character_images = CharacterImages()
		character_images.jpg = image
		
		mongo_character = Character()
		mongo_character.images = character_images
		mongo_character.name = jikan_character['name']
		mongo_character.name_kanji = jikan_character['name_kanji']
		mongo_character.nicknames = jikan_character['nicknames']
		mongo_character.rarity = raridade

		if acdb_character != None:
			mongo_character.gender = acdb_character['gender']

		return mongo_character
	
	def get_request_jikan(self, page) -> JikanRequest:

		character_request = JikanRequest()		
		character_request.page = page
		character_request.order_by = "favorites"
		character_request.sort = "desc"

		return character_request
	
	def get_request_acdb(self, character_name : str) -> AcdbRequest:

		character_request = AcdbRequest()		
		character_request.character_q = character_name

		return character_request
	
	def calcular_valores_raridade(self, total_personagens : int):

		percentuais = {
			0: 5,
			1: 25,
			2: 70
		}

		quantidades = {}
		
		for raridade, percentual in percentuais.items():
			quantidades[raridade] = (percentual / 100) * total_personagens

		return quantidades

	def get_raridade_personagem(self, raridades, indice_personagem):
		
		for valor_raridade, limite in raridades.items():
			if(indice_personagem <= limite):
				return valor_raridade


