import os

from exceptions import HelperEmailLabelFileNotExistsException

def load_email_label_file(email_label_file, encoding='utf8'):
	if not os.path.exists(email_label_file):
		raise HelperEmailLabelFileNotExistsException('email label file [%s] not exists' % email_label_file)
	labels = {}
	with open(email_label_file, 'r', encoding=encoding) as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			label, filename = line.split()
			label = label.strip()
			filename = filename.strip()
			if (not label) or (not filename):
				continue
			labels[filename] = int(label) # 1 -> non-spam email, 0 -> spam email
	return labels