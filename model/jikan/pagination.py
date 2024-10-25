from typing import List

from model.jikan.pagination_items import PaginationItems

class Pagination:

	def __init__(self):
		self.last_visible_page = 0
		self.has_next_page = False
		self.items: List[PaginationItems] = []
	
	def __init__(self, last_visible_page, has_next_page, items):
		self.last_visible_page = last_visible_page
		self.has_next_page = has_next_page
		self.items = items

