from typing import List

from infrastructure.mongo.character_repository import CharacterRepository
from infrastructure.anilist.character_api import CharacterApi as AnilistApi
from infrastructure.mongo.media_repository import MediaRepository

from model.mongo.character import Character
from model.mongo.character_images import CharacterImages
from model.mongo.image import Image
from model.mongo.media import Media
from character_dump.contador_personagens import ContadorPersonagens
from character_dump.limites_genero import LimitesGenero
from character_dump.limites_raridade import LimitesRaridade

class CharacterDump():

	def __init__(self) -> None:
		self.character_repository = CharacterRepository()		
		self.anilist_api = AnilistApi()
		self.media_repository = MediaRepository()
	
	def doDump(self, total_personagens, apagar_midia = False):

		self.character_repository.delete_all()

		limites_genero = LimitesGenero.create_limite_personagens(total_personagens, proporcao_mulheres=0.5)
		
		if(apagar_midia):
			self.media_repository.delete_all()

		contador_personagens = 0
		page = 0

		limites_raridade = LimitesRaridade.get_limites_raridade(total_personagens)		

		contador_personagens = ContadorPersonagens()

		page = 0

		while (contador_personagens.get_atual_total() ) < total_personagens:

			page += 1

			anilist_response = self.anilist_api.search(page)

			for anilist_character in anilist_response['data']['Page']['characters']:

				genero_personagem = anilist_character['gender']

				if (limites_genero.genero_ultrapassou_limite(genero_personagem, contador_personagens.get_by_genero(genero_personagem))):
					continue

				contador_personagens.adiciona_ao_genero(genero_personagem)

				indice_personagem = contador_personagens.get_by_genero_com_other(genero_personagem)

				raridade_personagem = limites_raridade.get_raridade_personagem(genero_personagem, indice_personagem)

				mongo_character = self.create_mongo_character(anilist_character, raridade_personagem)				
				
				self.character_repository.insert_waifu(mongo_character)

				if contador_personagens.get_atual_total() >= total_personagens:
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

		mongo_character.media_id = self.get_character_media_id(anilist_character['media'])		
		mongo_character.nicknames.extend(self.get_character_nickname_media(mongo_character.name, anilist_character['media']))

		return mongo_character

	def get_character_media_id(self, list_anilist_media) -> List[str]:
		list_media = []

		for anilist_media in list_anilist_media['nodes']:

			returned_media = self.media_repository.find_media_by_romaji(anilist_media['title'].get('romaji'))

			if(returned_media == None):
				mongo_media = Media()
				mongo_media.title.english = anilist_media['title'].get('english')
				mongo_media.title.native = anilist_media['title'].get('native')
				mongo_media.title.romaji = anilist_media['title'].get('romaji')
				mongo_media.title.user_preferred = anilist_media['title'].get('userPreferred')

				list_media.append(self.media_repository.insert_media(mongo_media))

			else:
				list_media.append(str(returned_media["_id"]))
		
		return list_media
	
	def get_character_nickname_media(self, character_name, list_anilist_media) -> List[str]:

		list_nicknames = []

		for anilist_media in list_anilist_media['nodes']:
			character_nickname = f'{character_name} ({anilist_media['title'].get('romaji')})'

			list_nicknames.append(character_nickname)
		
		return list_nicknames

		
