import urllib.parse
import json

from config.rest_config import RestConfig
from model.jikan.character_search_request import CharacterSearchRequest

class CharacterApi:

	def search(self, character_search_request : CharacterSearchRequest):

		#Define rate limiter
		session = RestConfig.get_jikan_limiter()
		headers = RestConfig.get_headers()

		url = urllib.parse.urljoin(RestConfig.BASE_URL_JIKAN, "characters")

		print(url)

		payload = {
			'page': character_search_request.page,
			'limit': character_search_request.limit,
			'q': character_search_request.q,
			'order_by': character_search_request.order_by,
			'sort': character_search_request.sort,
			'letter': character_search_request.letter
		}

		response = session.get(url, params=payload, headers=headers)

		return json.loads(response.text)