##
# base exceptions
##

# base exception
class BaseException(Exception):
	def __init__(self, *args, **kwargs):
		super(BaseException, self).__init__(args, kwargs)

# db base exception
class DbBaseException(BaseException):
	def __init__(self, *args, **kwargs):
		super(DbBaseException, self).__init__(args, kwargs)

# db email base exception
class DbEmailBaseException(DbBaseException):
	def __init__(self, *args, **kwargs):
		super(DbEmailBaseException, self).__init__(args, kwargs)

# model base exception
class ModelBaseException(BaseException):
	def __init__(self, *args, **kwargs):
		super(ModelBaseException, self).__init__(args, kwargs)

# model email base exception
class ModelEmailBaseException(ModelBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelEmailBaseException, self).__init__(args, kwargs)

# model indexer base exception
class ModelIndexerBaseException(ModelBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelIndexerBaseException, self).__init__(args, kwargs)

# model indexer_to_email base exception
class ModelIndexerToEmailBaseException(ModelBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelIndexerToEmailBaseException, self).__init__(args, kwargs)

# loader base exception
class LoaderBaseException(BaseException):
	def __init__(self, *args, **kwargs):
		super(LoaderBaseException, self).__init__(args, kwargs)

# loader email base exception
class LoaderEmailBaseException(LoaderBaseException):
	def __init__(self, *args, **kwargs):
		super(LoaderEmailBaseException, self).__init__(args, kwargs)

# helper base exception
class HelperBaseException(BaseException):
	def __init__(self, *args, **kwargs):
		super(HelperBaseException, self).__init__(args, kwargs)

##
# exceptions
##

# db email exceptions
class DbEmailDirNotExistsException(DbEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(DbEmailDirNotExistsException, self).__init__(args, kwargs)

class DbEmailLabelFileNotExistsException(DbEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(DbEmailLabelFileNotExistsException, self).__init__(args, kwargs)

class DbEmailCreatingTableErrorException(DbEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(DbEmailCreatingTableErrorException, self).__init__(args, kwargs)

class DbEmailInsertingTableErrorException(DbEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(DbEmailInsertingTableErrorException, self).__init__(args, kwargs)

# model email exceptions
class ModelEmailLabelInvalidException(ModelEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelEmailLabelInvalidException, self).__init__(args, kwargs)

class ModelEmailFileNotExistsException(ModelEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelEmailFileNotExistsException, self).__init__(args, kwargs)

class ModelEmailEncodingIncorrectException(ModelEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelEmailEncodingIncorrectException, self).__init__(args, kwargs)

class ModelEmailParsingErrorException(ModelEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(ModelEmailParsingErrorException, self).__init__(args, kwargs)

# loader email exceptions
class LoaderEmailDataDirNotExistsException(LoaderEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(LoaderEmailDataDirNotExistsExceptionn, self).__init__(args, kwargs)

class LoaderEmailLabelsInvalidException(LoaderEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(LoaderEmailLabelsInvalidException, self).__init__(args, kwargs)

class LoaderEmailDbConnectionInvalidException(LoaderEmailBaseException):
	def __init__(self, *args, **kwargs):
		super(LoaderEmailDbConnectionInvalidException, self).__init__(args, kwargs)

# helper exceptions
class HelperEmailLabelFileNotExistsException(HelperBaseException):
	def __init__(self, *args, **kwargs):
		super(HelperEmailLabelFileNotExistsException, self).__init__(args, kwargs)