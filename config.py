import os

EMAIL_CORPUS_DATA_DIR = os.sep.join(['corpus', 'TRAINING'])
EMAIL_CORPUS_LABEL_FILE = os.sep.join(['corpus', 'SPAMTrain.label'])
EMAIL_TABLE_NAME = 'email'
EMAIL_TRAINING_SIZE_FACTOR = 0.5
SQLITE_DB_FILE = os.sep.join(['db', 'dump.db'])
SQLITE_DB_MODE = 'debug'
INDEXER_PRIOR_KEY = '__prior__'
INDEXER_INVISIBLE_KEY = '__invisible__'
INDEXER_INVISIBLE_POSITION_FACTOR = 0.65
CROSS_VALIDATION_K_FOLD = 5