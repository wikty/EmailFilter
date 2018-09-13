import re

def remove_tags_html(text=''):
	return re.sub(r'<[^>]+?>', '', text)