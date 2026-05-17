import os
import secrets
import logging


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', r'./uploads/')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', str(16 * 1024 * 1024)))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'test_db.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_COMMIT_TEARDOWN = True


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_COMMIT_TEARDOWN = False


config_map = {
    'development': DevConfig,
    'production': ProdConfig,
}


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevConfig)


def setup_logging():
    env = os.getenv('FLASK_ENV', 'development')
    level = logging.DEBUG if env == 'development' else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('werkzeug').setLevel(logging.INFO)
