"""Settings Module."""
import os
import pymongo

from dotenv import load_dotenv
from .logger_settings import *

# Load env
# -----------------------------------------------------------------------------
ROOT_PATH = os.path.abspath('')
ENV = os.path.join(ROOT_PATH, '.env')
load_dotenv(ENV)

# MongoDB connection settings
# ----------------------------------------------------------------------------
MONGO_DB = os.environ.get('MONGODB', 'store-db')
MONGO_HOST_1 = os.environ.get('MONGO_HOST_1', 'mongodb-myapp')  # mongo
MONGO_PORT_1 = os.environ.get('MONGO_PORT_1', 27017)  # mongo
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', '')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')
MONGODB_AUTH_DB = os.environ.get('MONGODB_AUTH_DB')

prod_conn_string = (
    'mongodb://{host}:{port}/{db}?'
    'authSource={authsource}'.format(
        host=MONGO_HOST_1, port=MONGO_PORT_1, db=MONGO_DB,
        authsource=MONGODB_AUTH_DB)
)

base_mongo_client = pymongo.MongoClient(prod_conn_string)
mongo_client = base_mongo_client[MONGO_DB]

# Collections
#-------------------------------------------------------------------------------
Products = mongo_client.products
Orders = mongo_client.orders

#--------------------------------------------------------------------------------

ERROR_MESSAGE = 'Something went wrong. we are checking it'
SUCCESS_MESSAGE = 'Success.'

