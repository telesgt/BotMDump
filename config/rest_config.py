from requests_ratelimiter import LimiterSession

class RestConfig:
	BASE_URL_JIKAN="https://api.jikan.moe/v4/"
	BASE_URL_ACDB="https://www.animecharactersdatabase.com/"
	BASE_URL_ANILIST="https://graphql.anilist.co"
	
	@staticmethod
	def get_jikan_limiter() -> LimiterSession:
		return LimiterSession(per_second=1)
	
	def get_acdb_limiter() -> LimiterSession:
		return LimiterSession(per_second=1)
	
	def get_anilist_limiter() -> LimiterSession:
		return LimiterSession(per_minute=20)
	
	@staticmethod
	def get_headers():
		return {'User-Agent': 'macaco.dump'}