import pickle, json, random
from optparse import OptionParser

import config
from db import SQLiteDB
from model import EmailModel
from loader import EmailLoader, TokenLoader
from helper import load_email_label_file
from statmodel import EmailBayesian

# from predictor import predict_email, evaluate_model
# from extractor import extract_features
# from plot_stat import plot_email_header_stat, plot_email_body_stat, plot_cross_validation

# def dump_indexer(indexer):
# 	with open('indexer.json', 'w', encoding='utf8') as f:
# 		f.write(json.dumps(indexer, ensure_ascii=False, indent=4))

# def dump_kfold(fold_list):
# 	for i in range(len(fold_list)):
# 		fold = fold_list[i]
# 		filename = 'fold_%d.json' % (i+1)
# 		with open(filename, 'w', encoding='utf8') as f:
# 			f.write(json.dumps(fold, ensure_ascii=False, indent=4))

# def dump_email(subject, body, tokens, label):
# 	with open('email.json', 'w', encoding='utf8') as f:
# 		f.write(json.dumps({
# 			'subject': subject,
# 			'body': body,
# 			'tokens': tokens,
# 			'label': label
# 		}, ensure_ascii=False, indent=4))



if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-a', '--action', dest='action', help='action')
	parser.add_option('-d', '--data', dest='data', help='extra data about action')
	(options, args) = parser.parse_args()

	
	if options.action == 'load-table-email':
		db = SQLiteDB(config.SQLITE_DB_FILE, config.SQLITE_DB_MODE)
		email_labels = load_email_label_file(config.EMAIL_CORPUS_LABEL_FILE)
		loader = EmailLoader(config.EMAIL_CORPUS_DATA_DIR, email_labels, db)
		result = loader.load()
		print(result)
	elif options.action == 'load-table-token':
		db = SQLiteDB(config.SQLITE_DB_FILE, config.SQLITE_DB_MODE)
		loader = TokenLoader(db)
		result = loader.load()
		print(result)
	elif options.action == 'predict-email':
		db = SQLiteDB(config.SQLITE_DB_FILE, config.SQLITE_DB_MODE)
		email_id = random.randint(2001, 4000)
		eml = EmailModel()
		eml.load_from_db(db, email_id)
		d = eml.dump()
		d['tokens'] = [token.strip() for token in d['tokens'].split(',') if token.strip()]
		email_bayesian = EmailBayesian(1, 2000, db)
		result = email_bayesian.predict(d['to'], d['bcc'], d['cc'], d['tokens'])
		print('origin', d['label'])
		print('predict', result[0]>result[1])
	else:
		print('please input action argument')
		# db = SQLiteDB(SQLITE_DB_FILE, SQLITE_DB_MODE)
		# email_bayesian = EmailBayesian(1, 2000, db)
		# email_id = random.randint(2001, 4000)
		# eml = EmailModel.load_from_db(db, email_id).dump()
		# print('predict', email_bayesian.predict(eml))
		# print('origin', eml['label'])
	# if options.action == 'extract-features':
	# 	email_header_stat, email_body_stat = extract_features(
	# 		config.EMAIL_CORPUS_DATA_DIR, 
	# 		config.EMAIL_CORPUS_LABEL_FILE,
	# 		email_header_test
	# 	)
	# 	plot_email_header_stat(email_header_stat, len(email_header_test.keys()))
	# 	plot_email_body_stat(email_body_stat)
	# elif options.action == 'load-email':
	# 	total = load_email(
	# 		config.EMAIL_CORPUS_DATA_DIR, 
	# 		config.EMAIL_CORPUS_LABEL_FILE,
	# 		config.SQLITE_DB_FILE,
	# 		config.SQLITE_DB_MODE,
	# 		config.EMAIL_TABLE_NAME
	# 	)
	# 	print('load %d emails into database' % total)
	# elif options.action == 'load-indexer':
	# 	indexer = load_indexer(
	# 		config.SQLITE_DB_FILE,
	# 		config.SQLITE_DB_MODE,
	# 	 	config.EMAIL_TABLE_NAME,
	# 	 	config.INDEXER_PRIOR_KEY,
	# 		config.INDEXER_INVISIBLE_KEY,
	# 		config.INDEXER_INVISIBLE_POSITION_FACTOR
	# 	)
	# 	print('load indexer')
	# 	dump_indexer(indexer)
	# elif options.action == 'load-kfold':
	# 	fold_list = load_kfold(
	# 		config.SQLITE_DB_FILE,
	# 		config.SQLITE_DB_MODE,
	# 	 	config.EMAIL_TABLE_NAME,
	# 	 	config.INDEXER_PRIOR_KEY,
	# 		config.INDEXER_INVISIBLE_KEY,
	# 		config.INDEXER_INVISIBLE_POSITION_FACTOR,
	# 		config.CROSS_VALIDATION_K_FOLD
	# 	)
	# 	print('load k-fold')
	# 	dump_kfold(fold_list)
	# elif options.action == 'random-email':
	# 	subject, body, tokens, label = load_email_random(
	# 		config.EMAIL_CORPUS_DATA_DIR, 
	# 		config.EMAIL_CORPUS_LABEL_FILE
	# 	)
	# 	print('random email')
	# 	dump_email(subject, body, tokens, label)
	# elif options.action == 'predict-email':
	# 	subject, body, tokens, label = load_email_random(
	# 		config.EMAIL_CORPUS_DATA_DIR, 
	# 		config.EMAIL_CORPUS_LABEL_FILE
	# 	)
	# 	indexer = load_indexer(
	# 		config.SQLITE_DB_FILE,
	# 		config.SQLITE_DB_MODE,
	# 	 	config.EMAIL_TABLE_NAME,
	# 	 	config.INDEXER_PRIOR_KEY,
	# 		config.INDEXER_INVISIBLE_KEY,
	# 		config.INDEXER_INVISIBLE_POSITION_FACTOR
	# 	)
	# 	predict_label = predict_email(
	# 		tokens, 
	# 		indexer,
	# 		config.INDEXER_PRIOR_KEY,
	# 		config.INDEXER_INVISIBLE_KEY
	# 	)
	# 	print('email label: {}'.format(label))
	# 	print('predict label: {}'.format(predict_label))
	# elif options.action == 'cross-validate':
	# 	fold_list = load_kfold(
	# 		config.SQLITE_DB_FILE,
	# 		config.SQLITE_DB_MODE,
	# 	 	config.EMAIL_TABLE_NAME,
	# 	 	config.INDEXER_PRIOR_KEY,
	# 		config.INDEXER_INVISIBLE_KEY,
	# 		config.INDEXER_INVISIBLE_POSITION_FACTOR,
	# 		config.CROSS_VALIDATION_K_FOLD
	# 	)

	# 	# precision_sum = 0
	# 	# recall_sum = 0
	# 	precision_list = []
	# 	recall_list = []
	# 	for fold in fold_list:
	# 		indexer = fold['indexer']
	# 		emails = fold['emails']

	# 		precision, recall = evaluate_model(
	# 			indexer,
	# 			emails,
	# 			config.INDEXER_PRIOR_KEY,
	# 			config.INDEXER_INVISIBLE_KEY
	# 		)

	# 		# print('precision: %f' % precision)
	# 		# print('recall: %f' % recall)
	# 		precision_list.append(precision)
	# 		recall_list.append(recall)

	# 	plot_cross_validation(precision_list, recall_list)
	# 		# precision_sum += precision
	# 		# recall_sum += recall
		
	# 	# print('%d-fold cross validation average precision: %f' % (config.CROSS_VALIDATION_K_FOLD, precision_sum/len(fold_list)))
	# 	# print('%d-fold cross validation average recall: %f' % (config.CROSS_VALIDATION_K_FOLD, recall_sum/len(fold_list)))