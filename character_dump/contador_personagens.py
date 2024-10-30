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
	
	def get_by_genero_com_other(self, genero):

		if genero in self.quantidades_genero.keys():
			quantidade_genero = self.quantidades_genero.get(genero, 0)
			return quantidade_genero + self.quantidades_genero[ContadorPersonagens.OTHER_ID]
		else:
			total = 0
			for quantidades in self.quantidades_genero.values():
				total += quantidades
			return total

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

		if genero in self.quantidades_genero.keys():
			self.quantidades_genero[genero] += 1
		else:
			self.quantidades_genero[ContadorPersonagens.OTHER_ID] += 1