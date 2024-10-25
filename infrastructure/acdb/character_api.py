import urllib.parse

from config.rest_config import RestConfig
from model.acdb.character_search_request import CharacterSearchRequest

class CharacterApi:

	def __init__(self) -> None:
		self.session = RestConfig.get_acdb_limiter()
		self.custom_headers = RestConfig.get_headers()

	def find_by_name(self, request : CharacterSearchRequest):

		url = urllib.parse.urljoin(RestConfig.BASE_URL_ACDB, "api_series_characters.php")

		print(f"Consultando personagem ACDB {request.character_q}")

		payload = {
			'character_q': request.character_q			
		}

		response = self.session.get(url, params=payload, headers=self.custom_headers)

		if response.status_code != 200:
			raise Exception(f"Erro ao consultar personagem no ACDB {response.status_code} : {response.text}")
		
		if response.text == "-1":
			raise Exception(f"Personagem {request.character_q} nao encontrado ACDB {response.status_code} : {response.text}")

		return response.json()['search_results'][0]