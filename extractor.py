import os, email

from data_loader import extract_valid_tokens

def extract_features(email_dir, label_file, email_header_test):
	if not os.path.isdir(email_dir):
		raise Exception('email dir[%s] not exists' % email_dir)
	if not os.path.exists(label_file):
		raise Exception('label file[%s] not exists' % label_file)

	email_header_stat = {
		'positive': {key:0 for key in email_header_test},
		'negative': {key:0 for key in email_header_test}
	}
	email_body_stat = {
		'positive': {
			'__body__': ''
		},
		'negative': {
			'__body__': ''
		},
		'tokens': {}
	}

	token_id = 1
	with open(label_file, 'r', encoding='utf8') as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			label, filename = line.split()
			label = label.strip()
			filename = filename.strip()
			if (not label) or (not filename):
				continue
			label = int(label)
			with open(os.sep.join([email_dir, filename]), 'r', encoding='utf8') as f:
				try:
					raw = f.read() # file encoding not utf-8, will raise exception
				except Exception as e:
					continue
				msg = email.message_from_string(raw)
				for field in email_header_test:
					i = int(email_header_test[field](msg.get(field, '')))
					if label == 1:
						email_header_stat['positive'][field] += i
					else:
						email_header_stat['negative'][field] += i
				body = ''
				if not msg.is_multipart():
					body = msg.get_payload()
				else:
					for part in msg.walk():
						body += str(msg.get_payload())
				tokens = extract_valid_tokens(body)
				if label == 1:
					email_body_stat['positive']['__body__'] += ' '.join(tokens)
				else:
					email_body_stat['negative']['__body__'] += ' '.join(tokens)
				for token in tokens:
					if label == 1:
						t = email_body_stat['positive']
					else:
						t = email_body_stat['negative']
					if token not in email_body_stat['tokens']:
						email_body_stat['tokens'][token] = token_id
						token_id += 1
					if token not in t:
						t[token] = 0
					t[token] += 1
	
	return [email_header_stat, email_body_stat]