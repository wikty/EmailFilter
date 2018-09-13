def lowercase(tokens):
	if isinstance(tokens, list):
		return [str(token).lower() for token in tokens]
	else:
		return str(tokens).lower()

def uppercase(tokens):
	if isinstance(tokens, list):
		return [str(token).upper() for token in tokens]
	else:
		return str(tokens).upper()