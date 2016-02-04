import os

# FLASK
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(basedir, 'templates')
STATIC_DIR = os.path.join(basedir, 'static')
DATABASE = os.path.join(basedir, 'publickeykeeper.db')

# TWITTER
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', 'default_value')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', 'default_value')
TWITTER_APP_KEY = os.getenv('TWITTER_APP_KEY', 'default_value')
TWITTER_APP_KEY_SECRET = os.getenv('TWITTER_APP_KEY_SECRET', 'default_value')

# CELERY
CELERY_BROKER_CONNECTION_TIMEOUT = 20
CELERY_BROKER_POOL_LIMIT = 0
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
CELERY_CHORD_PROPAGATES = True
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IMPORTS = ('api.tasks',)
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_REDIS_MAX_CONNECTIONS = 1
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379')
CELERY_TASK_SERIALIZER = 'json'
