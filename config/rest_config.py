class RestConfig:
	BASE_URL_JIKAN="https://api.jikan.moe/v4/"

	def __setattr__(self, name, value):
		raise TypeError("Constants are immutable")