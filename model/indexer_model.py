import copy

from .base_model import BaseModel


class IndexerModel(BaseModel):
	@classmethod
	def table_name(cls):
		return 'indexer'

	@classmethod
	def table_definition(cls):
		return {
			'token': 's',
			'positive': 'i',
			'negative': 'i'
		}

	def __init__(self, fields={}):
		self.fields = {}
		if fields:
			self.load(fields)

	def dict(self):
		return copy.deepcopy(self.fields)