from flask import Flask
import os
import logging


class Logger(object):
	"""Logging information"""
	levels = {"debug":10,"info":20,"warning":30,"error":40,"critical":50}
	
	def __init__(self, name, filename, level):
		super(Logger, self).__init__()
		self.name = name
		self.filename = filename
		self.level = self.levels[level]

	def create_logger(self):
		"""
		Return a logger object with name, level and filename attributes of the object.
		"""
		logger_object = logging.getLogger(self.name)
		logger_object.setLevel(self.level)
		formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
		file = logging.FileHandler(self.filename)
		file.setFormatter(formatter)
		logger_object.addHandler(file)
		return logger_object


app = Flask(__name__)

# """ Initiating the logger"""

log_path = '/var/log/supervisor'
	
info_logger = Logger("info_logger", os.path.join(log_path, "info.log"), "info").create_logger()
error_logger = Logger("error_logger", os.path.join(log_path, "error.log"), "error").create_logger()
loggers = {"info":info_logger, "error":error_logger}

from app.api.controllers import api_file