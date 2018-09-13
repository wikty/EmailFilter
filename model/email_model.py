import os, email, copy

from .base_model import BaseModel

from exceptions import ModelEmailLabelInvalidException
from exceptions import ModelEmailFileNotExistsException
from exceptions import ModelEmailEncodingIncorrectException
from exceptions import ModelEmailParsingErrorException
from preprocessor import extract_valid_tokens_english


class EmailModel(BaseModel):

	@classmethod
	def table_name(cls):
		return 'email'

	@classmethod
	def table_definition(cls):
		return {
			'from': 's',
			'to': 's',
			'bcc': 's',
			'cc': 's',
			'message_id': 's',
			'subject': 's',
			'body': 's',
			'label': 'i',
			'tokens': 's',
			'raw': 's'
		}

	def __init__(self, fields={}):
		self.fields = {}
		if fields:
			self.load(fields)
		
	def dict(self):
		return copy.deepcopy(self.fields)
		# return {
		# 	'label': self.email_label,
		# 	'from': self.email_from,
		# 	'to': self.email_to,
		# 	'bcc': self.email_bcc,
		# 	'cc': self.email_cc,
		# 	'message_id': self.email_message_id,
		# 	'subject': self.email_subject,
		# 	'body': self.email_body,
		# 	'tokens': ', '.join(self.email_tokens),
		# 	'raw': self.email_raw
		# }

	def load_from_file(self, email_file, email_label, encoding='utf8'):
		valid_email_label = set([0, 1, '0', '1'])
		if email_label not in valid_email_label:
			raise ModelEmailLabelInvalidException('email label [{}] is invalid'.format(email_label))
		if not os.path.exists(email_file):
			raise ModelEmailFileNotExistsException('email file [%s] not exists' % email_file)
		email_label = int(email_label)
		email_file = email_file
		try:
			with open(email_file, 'r', encoding=encoding) as f:
				email_raw = f.read()
		except Exception as e:
			raise ModelEmailEncodingIncorrectException(e)

		try:
			msg = email.message_from_string(email_raw)
			email_from = msg.get('from', '')
			email_to = msg.get('to', '')
			email_bcc = msg.get('bcc', '')
			email_cc = msg.get('cc', '')
			email_message_id = msg.get('message-id', '')
			email_subject = msg.get('subject', '')
			email_body = str(msg.get_payload())
			email_tokens = extract_valid_tokens_english(email_body)
		except Exception as e:
			raise ModelEmailParsingErrorException('when parse email encounter error [%s]' % str(e))

		self.load({
			'label': email_label,
			'from': email_from,
			'to': email_to,
			'bcc': email_bcc,
			'cc': email_cc,
			'message_id': email_message_id,
			'subject': email_subject,
			'body': email_body,
			'tokens': ', '.join(email_tokens),
			'raw': email_raw
		})

	def load_from_db(self, db_client, email_id):
		row = db_client.select_table(
			self.__class__.table_name(), 
			['label', 'from', 'to', 'bcc', 'cc', 'message_id', 'subject', 'body', 'tokens', 'raw'], 
			'id={}'.format(email_id)
		)
		if row:
			row = row[0]
			self.load({
				'label': row[0],
				'from': row[1],
				'to': row[2],
				'bcc': row[3],
				'cc': row[4],
				'message_id': row[5],
				'subject': row[6],
				'body': row[7],
				'tokens': row[8],
				'raw': row[9]
			})
		