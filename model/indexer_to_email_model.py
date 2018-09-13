import copy

from .base_model import BaseModel
from exceptions import ModelIndexerToEmailArgumentErrorException
from exceptions import ModelIndexerToEmailFieldTypeErrorException

class IndexerToEmailModel(BaseModel):
	@classmethod
	def table_name(cls):
		return 'indexer_to_email'

	@classmethod
	def table_definition(cls):
		return {
			'email_id': 'i',
			'indexer_id': 'i'
		}

	def __init__(self, fields={}):
		self.fields = {}
		if fields:
			self.load(fields)

	def load(self, fields):
		if not isinstance(fields, dict):
			raise ModelIndexerToEmailArgumentErrorException('fields argument should be a dict')
		for fieldname in self.__class__.table_definition():
			if not self.check(fieldname, fields.get(fieldname)):
				raise ModelIndexerToEmailFieldTypeErrorException('model field type error: %s' % fieldname)
			self.fields[fieldname] = fields.get(fieldname)

	def dict(self):
		return copy.deepcopy(self.fields)