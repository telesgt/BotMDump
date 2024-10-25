import urllib.parse

from config.rest_config import RestConfig
from model.jikan.character_search_request import CharacterSearchRequest

class AnimeApi:

	def search(self, request : CharacterSearchRequest):

		#Define rate limiter
		session = RestConfig.get_jikan_limiter()
		custom_headers = RestConfig.get_headers()

		url = urllib.parse.urljoin(RestConfig.BASE_URL_JIKAN, "characters")

		print(f"Consultando pagina {request.page} do Jikan")

		payload = {
			'page': request.page,
			'limit': request.limit,
			'q': request.q,
			'order_by': request.order_by,
			'sort': request.sort,
			'letter': request.letter
		}

		response = session.get(url, params=payload, headers=custom_headers)

		if response.status_code != 200:
			raise Exception(f"Erro ao consultar personagens no Jikan {response.status_code} : {response.text}")

		return response.json()