class Image:

	def __init__(self):
		self.image_url = None
		self.small_image_url = None

	def __init__(self, image_url=None, small_image_url=None):
		self.image_url = image_url
		self.small_image_url = small_image_url