import logging
import sys

import config

# Define log levels
LOG_LEVELS = {
	'DEBUG':    logging.DEBUG,
	'INFO':     logging.INFO,
	'WARNING':  logging.WARNING,
	'ERROR':    logging.ERROR,
	'CRITICAL': logging.CRITICAL
}

# Set the log level based on config.log_level
log_level = LOG_LEVELS.get(config.log_level, logging.INFO)

# Create a logger
logger = logging.getLogger()
logger.setLevel(log_level)


# Create a formatter with colored output
# formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')


class ColoredConsoleHandler(logging.StreamHandler):
	COLORS = {
		'DEBUG':    '\033[0;36m',  # Cyan
		'INFO':     '\033[0;32m',  # Green
		'WARNING':  '\033[0;33m',  # Yellow
		'ERROR':    '\033[0;31m',  # Red
		'CRITICAL': '\033[0;35m',  # Purple
	}

	RESET = '\033[0m'

	def emit(self, record):
		try:
			message = self.format(record)
			stream = self.stream
			if record.levelname in self.COLORS:
				message = self.COLORS[record.levelname] + message + self.RESET
			stream.write(message + '\n')
			self.flush()
		except Exception:
			self.handleError(record)


console_handler = ColoredConsoleHandler()
console_handler.setLevel(log_level)
# console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


def log(message, log_type='INFO'):
	log_type = log_type.upper()

	if log_type not in LOG_LEVELS:
		log_type = 'INFO'

	# Use the built-in logging methods instead of manually checking log levels
	logging_method = getattr(logger, log_type.lower(), logger.info)
	logging_method(message)


def set_level(level):
	global log_level
	log_level = LOG_LEVELS.get(level, logging.INFO)
	logger.setLevel(log_level)
	console_handler.setLevel(log_level)
