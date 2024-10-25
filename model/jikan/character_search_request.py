class CharacterSearchRequest:

	page : int

	def __init__(self) -> None:	
		self.page = 0
		self.limit = 0
		self.q = ""
		self.order_by = "string" # todo fazer enum um dia
		self.sort = "" # todo fazer enum um dia
		self.letter = ""