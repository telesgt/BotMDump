class CharacterSearchRequest:

	def __init__(self):	
		self.page = None
		self.limit = None
		self.q = None
		self.order_by = "" # todo fazer enum um dia
		self.sort = "" # todo fazer enum um dia
		self.letter = None