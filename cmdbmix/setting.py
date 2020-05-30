import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')
    SQLALCHEMY_DATABASE_URI = "mysql://root:wlm@6291540@192.168.200.125:33060/cmdbmix"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}