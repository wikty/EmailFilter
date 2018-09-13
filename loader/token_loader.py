from model import EmailModel, TokenModel, TokenToEmailModel

class TokenLoader(object):
	def __init__(self, db_client):
		self.db_client = db_client
		self.positive_label = 1 # non-spam email
		self.negative_label = 0 # spam email

		self.tokens = []
		self.token_to_email = {}
		self.email_label = {}
		for row in db_client.select_table(EmailModel.table_name(), ['id', 'label', 'tokens']):
			email_id, label, tokens = int(row[0]), int(row[1]), row[2]
			tokens = set([token.strip() for token in tokens.split(',')]) # unique token
			self.email_label[email_id] = label
			for token in tokens:
				if not token:
					continue
				if token not in self.token_to_email:
					self.token_to_email[token] = set()
					tk = TokenModel()
					tk.load({
						'token': token
					})
					self.tokens.append(tk.dump())
				if email_id not in self.token_to_email[token]:
					self.token_to_email[token].add(email_id)

	def create_table(self):
		self.db_client.create_table(TokenModel.table_name(), TokenModel.table_definition())
		self.db_client.create_table(TokenToEmailModel.table_name(), TokenToEmailModel.table_definition())

	def insert_table(self):
		c1 = self.db_client.insert_many_table(
			TokenModel.table_name(), 
			TokenModel.table_definition().keys(),
			self.tokens
		)
		values = []
		for row in self.db_client.select_table(TokenModel.table_name(), ['id', 'token']):
			token_id, token = int(row[0]), row[1]
			for email_id in self.token_to_email[token]:
				values.append({
					'email_id': email_id,
					'token_id': token_id,
					'email_label': self.email_label[email_id]
				})
		c2 = self.db_client.insert_many_table(
			TokenToEmailModel.table_name(),
			TokenToEmailModel.table_definition().keys(),
			values
		)

		return c1+c2
	
	def load(self):
		self.create_table()
		return self.insert_table()