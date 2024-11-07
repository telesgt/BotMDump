from character_dump.contador_personagens import ContadorPersonagens
import math

class LimitesRaridade():

	def __init__(self):

		self.raridades = [0, 1, 2]

		self.limites = {
			ContadorPersonagens.FEMALE_ID: {},
			ContadorPersonagens.MALE_ID: {},
			ContadorPersonagens.OTHER_ID: {},
		}

		for genero in self.limites.keys():
			for raridade in self.raridades:
				self.limites[genero][raridade] = 0

	def set_limite_genero(self, genero, raridade, indice_limite):
		self.limites[genero][raridade] = indice_limite

	# calcula até qual indice de personagem deve aplicar determinada raridade
	# em seguida divide esse indice por 2 para definir quantos serão por genero, dando preferencia ao numero superior para feminino
	@staticmethod
	def get_limites_raridade(total_personagens : int):

		obj = LimitesRaridade()
		
		percentuais = {
			0: 5,
			1: 25,
			2: 70
		}
		
		indice_anterior_masculino = 0
		indice_anterior_feminino = 0

		for raridade, percentual in percentuais.items():

			limite_total = ((percentual / 100) * total_personagens)
			limite_genero_masculino = math.trunc(limite_total / 2)
			limite_genero_feminino = (limite_total - limite_genero_masculino)

			obj.set_limite_genero(ContadorPersonagens.MALE_ID, raridade, limite_genero_masculino + indice_anterior_masculino)
			obj.set_limite_genero(ContadorPersonagens.FEMALE_ID, raridade, limite_genero_feminino + indice_anterior_feminino)
			obj.set_limite_genero(ContadorPersonagens.OTHER_ID, raridade, limite_total + indice_anterior_feminino + indice_anterior_masculino)

			indice_anterior_masculino = limite_genero_masculino
			indice_anterior_feminino = limite_genero_feminino

		return obj
	
	# Busca o valor de raridade do personagem por genero
	# Se o genero nao for um dos padrões, irá considerar como se pertencesse aos dois ao mesmo tempo, e irá verificar o indice do personagem com 
	# a soma dos dois limites (Male e Female)
	def get_raridade_personagem(self, genero_str : str, indice_personagem : int) -> int:

		genero = ContadorPersonagens.OTHER_ID

		if genero_str in self.limites.keys():
			genero = genero_str

		for valor_raridade, indice_limite in self.limites[genero].items():
			if(indice_personagem <= indice_limite):
				return valor_raridade
		
		return 2

		
		