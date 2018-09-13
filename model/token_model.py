import copy

from .base_model import BaseModel


class TokenModel(BaseModel):
	@classmethod
	def table_name(cls):
		return 'token'

	@classmethod
	def table_definition(cls):
		return {
			'token': 's'
		}

	def __init__(self, fields={}):
		self.fields = {}
		if fields:
			self.load(fields)

	def dict(self):
		return copy.deepcopy(self.fields)