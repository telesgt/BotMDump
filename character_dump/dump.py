from typing import List

from infrastructure.mongo.character_repository import CharacterRepository
from infrastructure.anilist.character_api import CharacterApi as AnilistApi
from infrastructure.mongo.media_repository import MediaRepository

from model.mongo.character import Character
from model.mongo.character_images import CharacterImages
from model.mongo.image import Image
from model.mongo.media import Media

class ContadorPersonagens():

	FEMALE_ID='Female'
	MALE_ID='Male'
	OTHER_ID='Other'

	def __init__(self):
		self.quantidades_genero = {
			ContadorPersonagens.FEMALE_ID: 0,
			ContadorPersonagens.MALE_ID: 0,
			ContadorPersonagens.OTHER_ID: 0
		}
	
	def get_by_genero(self, genero):
		return self.quantidades_genero.get(genero, self.quantidades_genero[ContadorPersonagens.OTHER_ID])

	def get_atual_feminino(self) -> int:
		return self.get_by_genero[ContadorPersonagens.FEMALE_ID] + self.get_by_genero[ContadorPersonagens.OTHER_ID]
	
	def get_atual_masculino(self) -> int:
		return self.get_by_genero[ContadorPersonagens.MALE_ID] + self.get_by_genero[ContadorPersonagens.OTHER_ID]
	
	def get_atual_total(self) -> int:
		atual_total = 0

		for quantidade_atual_genero in self.quantidades_genero.values():
			atual_total += quantidade_atual_genero

		return atual_total
	
	def adiciona_ao_genero(self, genero):

		if genero in self.quantidades_genero:
			self.quantidades_genero[genero] += 1
		else:
			self.quantidades_genero[ContadorPersonagens.MALE_ID] += 1

		

class LimitesGenero():
	
	def __init__(self, quantidade_mulheres, quantidade_homens, quantidade_outros):
		self.limites = {
			ContadorPersonagens.FEMALE_ID: quantidade_mulheres,
			ContadorPersonagens.MALE_ID: quantidade_homens,
			ContadorPersonagens.OTHER_ID: quantidade_outros
		}

	def get_limite_genero(self, genero) -> int:
		return self.limites.get(genero, self.limites[ContadorPersonagens.OTHER_ID])

class CharacterDump():

	def __init__(self) -> None:
		self.character_repository = CharacterRepository()		
		self.anilist_api = AnilistApi()
		self.media_repository = MediaRepository()
	
	def doDump(self, total_personagens, apagar_midia = False):

		self.character_repository.delete_all()

		limites_genero = self.get_limite_personagens_por_genero(total_personagens, proporcao_mulheres=0.5)
		
		if(apagar_midia):
			self.media_repository.delete_all()

		contador_personagens = 0
		page = 0
		limites_raridade = self.calcular_limites_raridade(total_personagens)

		contador_personagens = ContadorPersonagens()

		page = 0

		while (contador_personagens.get_atual_total() ) < total_personagens:

			page += 1

			anilist_response = self.anilist_api.search(page)

			for anilist_character in anilist_response['data']['Page']['characters']:

				genero_personagem = anilist_character['gender']

				if (self.genero_ultrapassou_limite(limites_genero, genero_personagem, contador_personagens.get_by_genero(genero_personagem))):
					continue

				contador_personagens.adiciona_ao_genero(genero_personagem)

				mongo_character = self.create_mongo_character(anilist_character, raridade=self.get_raridade_personagem(limites_raridade, contador_personagens.get_atual_total()))				
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

	def get_raridade_personagem(self, raridades, indice_personagem : int):
		
		for valor_raridade, indice_limite in raridades.items():
			if(indice_personagem <= indice_limite):
				return valor_raridade

	# Define a proporcao de personagens para cada genero. 
	# Se passar a proporcao de mulheres, a de homens sera ignorada
	# Se passar
	def get_limite_personagens_por_genero(self, total_personagens : int, proporcao_mulheres : float = 0, proporcao_homens : float = 0) -> LimitesGenero:

		quantidade_mulheres = 0
		quantidade_homens = 0
		
		if(proporcao_mulheres > 0):
			quantidade_mulheres = total_personagens * proporcao_mulheres
			quantidade_homens = total_personagens - quantidade_mulheres
		else:
			quantidade_homens = total_personagens * proporcao_mulheres
			quantidade_mulheres = total_personagens - quantidade_homens

		return LimitesGenero(quantidade_mulheres, quantidade_homens, total_personagens)
	
	def genero_ultrapassou_limite(self, limites_genero : LimitesGenero, genero_personagem : str, quantidade_atual : int):

		limite_genero = limites_genero.get_limite_genero(genero_personagem)

		return quantidade_atual >= limite_genero

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

		
