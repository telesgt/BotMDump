from config.rest_config import RestConfig

class CharacterApi:

	def __init__(self) -> None:
		self.session = RestConfig.get_anilist_limiter()
		self.custom_headers = RestConfig.get_headers()

	def search(self, page : int):

		query = '''
			query ($id: Int, $page: Int, $perPage: Int, $sort: [CharacterSort]) {
				Page (page: $page, perPage: $perPage) {
					pageInfo {
						currentPage
						hasNextPage
						perPage
					}
					characters (id: $id, sort: $sort) {
						id
						name {
							full
							native
							alternative
							}
						gender
						favourites
						image {
							large
							medium
						}
						media {
							nodes {
								title {
									english
									native
									romaji
									userPreferred
								}
							}
						}
					}
				}
			}
			'''

		variables = {
			"sort": "FAVOURITES_DESC",
			"page": page,
			"perPage": 50
		}

		payload = {
			"query": query,
			"variables": variables
		}

		print(f"Consultando pagina {page} do Anilist")

		response = self.session.post(RestConfig.BASE_URL_ANILIST, json=payload, headers=self.custom_headers)

		if response.status_code != 200:
			raise Exception(f"Erro ao consultar personagem no ANILIST {response.status_code} : {response.text} : {response.headers.get("X-RateLimit-Remaining")} : {response.headers.get("X-Rety-After")}")
		
		return response.json()
