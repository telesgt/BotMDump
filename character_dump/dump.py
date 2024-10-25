import requests
import requests_ratelimiter

from infrastructure.jikan.character_repository import CharacterRepository
from model.jikan.character_search_request import CharacterSearchRequest

class CharacterDump():
	
	def doDump(self):

		test = CharacterRepository()

		character_request = CharacterSearchRequest()
		character_request.limit = 25
		character_request.page = 1
		character_request.order_by = "favorites"
		character_request.sort = "desc"

		test.search(character_request)