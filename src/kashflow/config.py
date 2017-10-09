class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = '127.0.0.1:27017'
    DATABASE = 'kashflow'
    PLAID_KEYS = ''


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DATABASE = 'kashflow-test'

