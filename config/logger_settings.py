"""Module: Logger Settings."""
import os
import sys
import logging

from logging.config import dictConfig

ROOT_DIR = os.path.abspath('.')

# Creating logs directory
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')

try:
    print('INFO  * Creating logs Directory: {}'.format(LOGS_DIR))
    os.mkdir(LOGS_DIR)
except FileExistsError:
    print('INFO  * {}: Directory already exists'.format(LOGS_DIR))

required_loggers = ['app']

handlers = {}
all_loggers = {}

for r_logger in required_loggers:
    # handlers
    handlers[r_logger] = {
        'class': 'logging.FileHandler',
        'formatter': 'verbose',
        'level': logging.DEBUG,
        'filename': 'logs/{}.log'.format(r_logger),
        # 'when': 'MIDNIGHT',
        # 'maxBytes': 52428800,
        # 'backupCount': 7
    }
    # create loggers
    all_loggers['{}_logger'.format(r_logger)] = {
        'handlers': [r_logger, 'console'],
        'level': logging.DEBUG
    }

handlers['console'] = {
    'class': 'logging.StreamHandler',
    'level': 'DEBUG',
    'formatter': 'simple',
    'stream': sys.stdout,
}

all_loggers['werkzeug'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': True,
}

logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers=handlers,
    loggers=all_loggers
)

dictConfig(logging_config)

app_logger = logging.getLogger('app_logger')