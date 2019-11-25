"""
	Support for images in openNCEM  supported 
	file formats: *.emd and *.ser
"""

# standard libraries
import gettext
import pathlib
import logging

# third party libraries

# local libraries
from .ncem_image_utils import loadSER, loadEMD

_ = gettext.gettext


class OpenNCEMDelegate(object):

	def __init__(self,api):
		self.__api = api
		self.io_handler_id = "openNCEM-io-handler"
		self.io_handler_name = _("openNCEM Supported")
		self.io_handler_extensions = ["emd", "ser", "h5"]



	def read_data_and_metadata(self, extension, file_path):
		logging.debug('entered read data_and_metadata')
		assert extension in ['ser','emd','h5'], 'Unsupported extension'

		if extension == 'ser':
			return loadSER(file_path)
		if extension in ['h5','emd']:
			return loadEMD(file_path)
		# if extension == 'mrc':
		# 	return loadMRC(file_path)


	def can_write_data_and_metadata(self, data_and_metadata, extension):
		logging.debug('entered can_write_data_and_metadata')
		return None

	def write_data_and_metadata(self, data_and_metadata, file_path_str: str, extension):
		logging.debug('entered write_data_and_metadata')





class OpenNCEMExtension(object):

	# required for Swift to recognize this as an extension class.
	extension_id = "openNCEM.swift.extensions.filetypes"

	def __init__(self, api_broker):
		#logging.debug('started an openNCEM extension...')
		# grab the api object.
		api = api_broker.get_api(version="1", ui_version="1")
		# be sure to keep a reference or it will be closed immediately.
		self.__io_handler_ref = api.create_data_and_metadata_io_handler(OpenNCEMDelegate(api))


	def close(self):
		# close will be called when the extension is unloaded. in turn, close any references so they get closed. this
		# is not strictly necessary since the references will be deleted naturally when this object is deleted.
		self.__io_handler_ref.close()
		self.__io_handler_ref = None