from model.jikan.character_images import CharacterImages

class Character:

	def __init__(self):
		self.mal_id = 0
		self.url = ""
		self.images = CharacterImages()
		self.name = ""
		self.name_kanji = ""
		self.nicknames = []
		self.favorites = 0
		self.about = ""