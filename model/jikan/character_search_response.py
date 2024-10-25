from typing import List

from model.jikan.pagination import Pagination

class CharacterSearchResponse:

	def __init__(self):
		# self.data = List[Character] = []
		self.pagination = Pagination()