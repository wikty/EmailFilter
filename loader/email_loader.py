import os

from model import EmailModel
from exceptions import LoaderEmailDataDirNotExistsException
from exceptions import LoaderEmailLabelsInvalidException
from exceptions import LoaderEmailDbConnectionInvalidException
from exceptions import ModelEmailBaseException

class EmailLoader(object):

	def __init__(self, email_dir, email_labels, db_client):
		if not os.path.isdir(email_dir):
			raise LoaderEmailDataDirNotExistsException('email dir [%s] not exists' % email_dir)
		if not isinstance(email_labels, dict):
			raise LoaderEmailLabelsInvalidException('email lables dictinoary is invalid')
		if not db_client:
			raise LoaderEmailDbConnectionInvalidException('db connection is invalid')
		self.email_dir = email_dir
		self.db_client = db_client
		self.email_labels = email_labels

	def create_table(self):
		self.db_client.create_table(EmailModel.table_name(), EmailModel.table_definition())

	def insert_table(self, gen):
		return self.db_client.insert_many_table(
			EmailModel.table_name(), 
			EmailModel.table_definition().keys(),
			gen
		)

	def get_generator(self):
		for email_file in self.email_labels:
			label = self.email_labels[email_file]
			email_file = os.sep.join([self.email_dir, email_file])
			try:
				eml = EmailModel()
				eml.load_from_file(email_file, label)
			except ModelEmailBaseException as e:
				print(e)
				continue
			yield eml.dump()

	def load(self):
		self.create_table()
		return self.insert_table(self.get_generator())