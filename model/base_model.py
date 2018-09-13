import abc

from exceptions import ModelBaseException

class BaseModel(object):
	__metaclass__ = abc.ABCMeta

	@classmethod
	@abc.abstractmethod
	def table_name(cls):
		'''
		Return model's table name(a str)
		'''
		return "Should Never See This"

	@classmethod
	@abc.abstractmethod
	def table_definition(cls):
		'''
		Return mode's table definition(a dict)
		'''
		return {"key":"Should Never See This"}

	# @property
	# def _fields(self):
	# 	return list(self.__class__.table_definition().keys())

	@abc.abstractmethod
	def dict(self):
		'''
		Return model fields and values(a dict has same keys with table_definition)
		'''
		return {field:None for field in self.__class__.table_definition().keys()}

	def check(self, field_name, field_value):
		if field_name not in self.__class__.table_definition():
			return False
		field_type = self.__class__.table_definition()[field_name]
		if field_type == 'i' and isinstance(field_value, int):
			return True
		elif field_type == 'f' and isinstance(field_value, float):
			return True
		elif field_type == 'd' and isinstance(field_value, float):
			return True
		elif field_type == 's' and isinstance(field_value, str):
			return True
		elif field_type == 'b' and isinstance(field_value, bool):
			return True
		elif field_type == 'n' and field_value is None:
			return True
		return False

	def dump(self):
		if set(self.dict().keys()) != set(self.__class__.table_definition().keys()):
			raise ModelBaseException("model [%s]'s dict method should has same keys with table definition" % self.__class__.__name__)

		return self.dict()

	def load(self, fields):
		if not isinstance(fields, dict):
			raise ModelBaseException('fields argument should be a dict')
		for fieldname in self.__class__.table_definition():
			if not self.check(fieldname, fields.get(fieldname)):
				raise ModelBaseException('model field type error: %s' % fieldname)
			self.fields[fieldname] = fields.get(fieldname)