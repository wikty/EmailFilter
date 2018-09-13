import os

EMAIL_CORPUS_DATA_DIR = os.sep.join(['corpus', 'TRAINING'])
EMAIL_CORPUS_LABEL_FILE = os.sep.join(['corpus', 'SPAMTrain.label'])

SQLITE_DB_FILE = 'dump.db'
SQLITE_DB_MODE = 'debug'

CROSS_VALIDATION_K_FOLD = 5