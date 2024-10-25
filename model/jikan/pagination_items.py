class PaginationItems:

	def __init__(self):
		self.count = 0
		self.total = 0
		self.per_page = 0

	def __init__(self, count, total, per_page):
		self.count = count
		self.total = total
		self.per_page = per_page