import math

from model import EmailModel
from model import TokenModel
from model import TokenToEmailModel

class EmailBayesian(object):

	def __init__(self, start_id, end_id, db_client):
		self.positive_label = 1
		self.negative_label = 0
		self.smooth_factor = 1
		self.email_header_cc_limit = 10
		self.email_header_bcc_limit = 10
		self.email_smooth = '____smooth____'
		self.email_prior = '____prior____'
		self.email_header_cc = '____cc____'
		self.email_header_bcc = '____bcc____'
		self.email_header_to = '____to____'
		self.stat = {}
		self.stat[self.email_smooth] = { '+': self.smooth_factor, '-': self.smooth_factor }
		self.stat[self.email_prior] = { '+': self.smooth_factor, '-': self.smooth_factor }
		self.stat[self.email_header_cc] = { '+': self.smooth_factor, '-': self.smooth_factor }
		self.stat[self.email_header_bcc] = { '+': self.smooth_factor, '-': self.smooth_factor }
		self.stat[self.email_header_to] = { '+': self.smooth_factor, '-': self.smooth_factor }
		where = 'id>=%d and id<=%d' % (start_id, end_id)
		for row in db_client.select_table(EmailModel.table_name(), ['label', 'cc', 'bcc', 'to'], where):
			label, cc, bcc, to = int(row[0]), row[1], row[2], row[3]
			if label == 1:
				self.stat[self.email_prior]['+'] += 1
			else:
				self.stat[self.email_prior]['-'] += 1
			if self.test_email_header_cc(cc):
				if label == 1:
					self.stat[self.email_header_cc]['+'] += 1
				else:
					self.stat[self.email_header_cc]['-'] += 1
			if self.test_email_header_bcc(bcc):
				if label == 1:
					self.stat[self.email_header_bcc]['+'] += 1
				else:
					self.stat[self.email_header_bcc]['-'] += 1
			if self.test_email_header_to(to):
				if label == 1:
					self.stat[self.email_header_to]['+'] += 1
				else:
					self.stat[self.email_header_to]['-'] += 1
		
		sql = 'SELECT token, SUM(email_label), COUNT(*) FROM `{tbl_token}` JOIN `{tbl_token_to_email}` ON `{tbl_token}`.id=`{tbl_token_to_email}`.token_id GROUP BY token_id'.format(
			tbl_token=TokenModel.table_name(),
			tbl_token_to_email=TokenToEmailModel.table_name()
		)
		for row in db_client.sql(sql):
			token, positive_count, total_count = row[0], row[1], row[2]
			negative_count = self.smooth_factor + total_count - positive_count
			positive_count += self.smooth_factor

			self.stat[token] = {
				'+': positive_count,
				'-': negative_count
			}

	def get_count(self, key):
		if key in self.stat:
			return (self.stat[key]['+'], self.stat[key]['-'])
		else:
			return (self.stat[self.email_smooth]['+'], self.stat[self.email_smooth]['-'])

	def predict(self, email_to, email_bcc, email_cc, email_tokens):
		# prior
		email_prior = self.get_count(self.email_prior)
		positive_probability = math.log(email_prior[0]/(email_prior[0]+email_prior[1]))
		negative_probability = math.log(email_prior[1]/(email_prior[0]+email_prior[1]))
		
		# likelihood
		prior_log_count = 0
		if self.test_email_header_cc(email_cc):
			cc_count = self.get_count(self.email_header_cc)
		else:
			cc_count = self.get_count(None)
		# math.log(cc_count[0]/email_prior[0]) = math.log(cc_count[0]) - math.log(email_prior[0])
		positive_probability += math.log(cc_count[0]) 
		negative_probability += math.log(cc_count[1])
		prior_log_count += 1

		if self.test_email_header_cc(email_bcc):
			bcc_count = self.get_count(self.email_header_bcc)
		else:
			bcc_count = self.get_count(None)
		positive_probability += math.log(bcc_count[0])
		negative_probability += math.log(bcc_count[1])
		prior_log_count += 1

		if self.test_email_header_to(email_to):
			to_count = self.get_count(self.email_header_to)
		else:
			to_count = self.get_count(None)
		positive_probability += math.log(to_count[0])
		negative_probability += math.log(to_count[1])
		prior_log_count += 1

		for token in email_tokens:
			token_count = self.get_count(token)
			positive_probability += math.log(token_count[0])
			negative_probability += math.log(token_count[1])
			prior_log_count += 1

		positive_probability -= math.log(email_prior[0])*prior_log_count
		negative_probability -= math.log(email_prior[1])*prior_log_count
		
		return (positive_probability, negative_probability)

	def test_email_header_cc(self, value):
		value = str(value)
		return bool(value) and len(value.split('@')) > self.email_header_cc_limit

	def test_email_header_bcc(self, value):
		value = str(value)
		return bool(value)

	def test_email_header_to(self, value):
		value = str(value)
		return bool(value) and len(value.split('@')) > self.email_header_bcc_limit