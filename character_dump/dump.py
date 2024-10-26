from infrastructure.mongo.character_repository import CharacterRepository
from infrastructure.anilist.character_api import CharacterApi as AnilistApi

from model.mongo.character import Character
from model.mongo.character_images import CharacterImages
from model.mongo.image import Image

class CharacterDump():

	def __init__(self) -> None:
		self.character_repository = CharacterRepository()		
		self.anilist_api = AnilistApi()
	
	def doDump(self, total_personagens):

		print('Limpando collection waifu')

		self.character_repository.delete_all()

		contador_personagens = 0
		page = 0
		limites_raridade = self.calcular_limites_raridade(total_personagens)

		while contador_personagens < total_personagens:

			page += 1

			anilist_response = self.anilist_api.search(page)

			for anilist_character in anilist_response['data']['Page']['characters']:

				contador_personagens += 1				

				mongo_character = self.create_mongo_character(anilist_character, raridade=self.get_raridade_personagem(limites_raridade, contador_personagens))
				self.character_repository.insert_waifu(mongo_character)

				if contador_personagens >= total_personagens:
					break
			
			if anilist_response['data']['Page']['pageInfo']['hasNextPage'] == False:
				print('Sem mais personagens para buscar')
				break

			

	def create_mongo_character(self, anilist_character, raridade=None) -> Character:

		image = Image()
		image.image_url = anilist_character['image']['large']
		image.small_image_url = anilist_character['image']['medium']

		character_images = CharacterImages()
		character_images.jpg = image
		
		mongo_character = Character()
		mongo_character.images = character_images
		mongo_character.name = anilist_character['name']['full']
		mongo_character.name_kanji = anilist_character['name']['native']
		mongo_character.nicknames = anilist_character['name']['alternative']
		mongo_character.gender = anilist_character['gender']
		mongo_character.rarity = raridade		

		return mongo_character	
	
	def calcular_limites_raridade(self, total_personagens : int):

		percentuais = {
			0: 5,
			1: 25,
			2: 70
		}

		limites = {}
		
		# calcula até qual indice de personagem deve aplicar determinada raridade

		indice_anterior = 0

		for raridade, percentual in percentuais.items():
			limites[raridade] = ((percentual / 100) * total_personagens) + indice_anterior
			indice_anterior = limites[raridade]

		return limites

	def get_raridade_personagem(self, raridades, indice_personagem):
		
		for valor_raridade, indice_limite in raridades.items():
			if(indice_personagem <= indice_limite):
				return valor_raridade