import copy

from .base_model import BaseModel


class TokenToEmailModel(BaseModel):
	@classmethod
	def table_name(cls):
		return 'token_to_email'

	@classmethod
	def table_definition(cls):
		return {
			'email_id': 'i',
			'token_id': 'i',
			'email_label': 'i'
		}

	def __init__(self, fields={}):
		self.fields = {}
		if fields:
			self.load(fields)

	def dict(self):
		return copy.deepcopy(self.fields)