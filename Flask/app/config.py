import os
import secrets
import logging


secret_key = secrets.token_hex(16)  # 生成一个16字节的随机字符串作为密钥
upload_dir = r'./uploads/'  # 设置上传文件的存储目录
file_up_load_size = 16 * 1024 * 1024  # 设置最大上传大小，例如16MB
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = 'sqlite:///' + os.path.join(basedir, 'test_db.db')


class Config:
    SECRET_KEY = secret_key
    DEBUG = True
    UPLOAD_FOLDER = upload_dir
    MAX_CONTENT_LENGTH = file_up_load_size
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True


def setup_logging():
    """
    Set up logging configuration for the Flask application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    # Suppress werkzeug logs
    logging.getLogger('werkzeug').setLevel(logging.INFO)
