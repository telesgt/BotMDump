from requests_ratelimiter import LimiterSession

class RestConfig:
	BASE_URL_JIKAN="https://api.jikan.moe/v4/"

	def __setattr__(self, name, value):
		raise TypeError("Constants are immutable")
	
	@staticmethod
	def get_jikan_limiter() -> LimiterSession:
		return LimiterSession(per_second=3, per_minute=60)
	
	@staticmethod
	def get_headers():
		headers = {'User-Agent': 'macaco.dump'}