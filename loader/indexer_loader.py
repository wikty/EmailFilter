from model import EmailModel, IndexerModel, IndexerToEmailModel

class IndexerLoader(object):
	def __init__(self, db_client):
		self.db_client = db_client
		self.positive_label = 1 # non-spam email
		self.negative_label = 0 # spam email

	def create_table(self):
		self.db_client.create_table(IndexerModel.table_name(), IndexerModel.table_definition())
		self.db_client.create_table(IndexerToEmailModel.table_name(), IndexerToEmailModel.table_definition())

	def insert_table(self):
		indexer = {}
		positive_label = self.positive_label
		negative_label = self.negative_label
		db_client = self.db_client
		
		for row in db_client.select_table(EmailModel.table_name(), ['id', 'label', 'tokens']):
			email_id, label, tokens = int(row[0]), int(row[1]), row[2]
			tokens = set([token.strip() for token in tokens.split(',')]) # unique token
			for token in tokens:
				if not token:
					continue
				if token not in indexer:
					indexer[token] = set()
				if email_id not in indexer[token]:
					indexer[token].add(email_id)

		for token in indexer:
			idx = IndexerModel()
			idx.load({
				'token': token,
				'positive': indexer[token]['positive'],
				'negative': indexer[token]['negative']
			})
			indexer_id = db_client.insert_table(IndexerModel.table_name(), idx.dump())
			for email_id in indexer[token]['emails']:
				i2e = IndexerToEmailModel()
				i2e.load({
					'email_id': email_id,
					'indexer_id': indexer_id
				})
				db_client.insert_table(IndexerToEmailModel.table_name(), i2e.dump())
	
	def load(self):
		self.create_table()
		return self.insert_table()