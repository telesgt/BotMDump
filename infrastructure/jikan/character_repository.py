import requests
import requests_ratelimiter
import urllib.parse

from config.rest_config import RestConfig
from model.jikan.character import Character
from model.jikan.character_search_request import CharacterSearchRequest

class CharacterRepository:

	def search(self, characterSearchRequest : CharacterSearchRequest):

		print(RestConfig.BASE_URL_JIKAN)

		url = urllib.parse.urljoin(RestConfig.BASE_URL_JIKAN, "characters")

		print(url)

		payload = {
			'page': characterSearchRequest.page,
			'limit': characterSearchRequest.limit,
			'q': characterSearchRequest.q,
			'order_by': characterSearchRequest.order_by,
			'sort': characterSearchRequest.sort,
			'letter': characterSearchRequest.letter
		}

		print(payload)

		response = requests.get(url, params=payload)

		print(response.text)


