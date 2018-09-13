import re

split_pattern = r'''(?x)  # set flag to allow verbose regexps
	(?:[A-Z]\.)+          # abbreviations, e.g. U.S.A.
	| \w+(?:-\w+)*        # words with optional internal hyphens
	| \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
	| \.\.\.              # ellipsis
	| [][.,;"'?():_`-]    # these are separate tokens; includes ], [
'''

def word_tokenize_english(text=''):
	if not text:
		return []

	tokens = []
	# positions = []
	for m in re.finditer(split_pattern, text):
		start = m.start()
		end = m.end()
		tokens.append(text[start:end])
		# positions.append([start, end])
	return tokens