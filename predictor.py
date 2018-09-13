def predict_email(email_tokens, indexer, prior_key, invisible_key):
	positive_probability = indexer[prior_key]['positive']
	negative_probability = indexer[prior_key]['negative']
	for token in set(email_tokens):
		pp = 0
		np = 0
		if token in indexer:
			pp = indexer[token]['positive']
			np = indexer[token]['negative']
		if pp == 0:
			pp = indexer[invisible_key]['positive']
		if np == 0:
			np = indexer[invisible_key]['negative']
		positive_probability *= pp
		negative_probability *= np
	return 1 if positive_probability > negative_probability else 0

def evaluate_model(indexer, emails, prior_key, invisible_key):
	precision = 0
	recall = 0
	true_positive = 0
	false_positive = 0
	false_negative = 0


	for email in emails:
		email_label = email[0]
		email_tokens = [token.strip() for token in email[1].split(',')]
		predict_label = predict_email(email_tokens, indexer, prior_key, invisible_key)
		if predict_label == 1:
			if email_label == 1:
				true_positive += 1
			else:
				false_positive += 1
		else:
			if email_label == 1:
				false_negative += 1
	precision = true_positive / (true_positive + false_positive)
	recall = true_positive / (true_positive + false_negative)

	return [precision, recall]