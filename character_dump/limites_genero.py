from character_dump.contador_personagens import ContadorPersonagens

class LimitesGenero():
	
	def __init__(self, quantidade_mulheres, quantidade_homens, quantidade_outros):
		self.limites = {
			ContadorPersonagens.FEMALE_ID: quantidade_mulheres,
			ContadorPersonagens.MALE_ID: quantidade_homens,
			ContadorPersonagens.OTHER_ID: quantidade_outros
		}

	def get_limite_genero(self, genero) -> int:
		return self.limites.get(genero, self.limites[ContadorPersonagens.OTHER_ID])
	
	def genero_ultrapassou_limite(self, genero_personagem : str, quantidade_atual : int):

		limite_genero = self.get_limite_genero(genero_personagem)
		return quantidade_atual >= limite_genero
	
	# Define a proporcao de personagens para cada genero. 
	# Se passar a proporcao de mulheres, a de homens sera ignorada
	# Para funcionar a proporcao de homens, deixar a de mulher como 0
	@staticmethod
	def create_limite_personagens(total_personagens : int, proporcao_mulheres : float = 0, proporcao_homens : float = 0):
		quantidade_mulheres = 0
		quantidade_homens = 0
		
		if(proporcao_mulheres > 0):
			quantidade_mulheres = total_personagens * proporcao_mulheres
			quantidade_homens = total_personagens - quantidade_mulheres
		else:
			quantidade_homens = total_personagens * proporcao_homens
			quantidade_mulheres = total_personagens - quantidade_homens

		return LimitesGenero(quantidade_mulheres, quantidade_homens, total_personagens)