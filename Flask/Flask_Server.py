# This is a demo for using libs (flask and sqlalchemy)
# Using flask and sqlalchemy create, select, query, update sqlite
#  Next step, will focus on Web UI(html, css, javascript)
import pathlib
import secrets

from flask import Flask


FILE = pathlib.Path(__file__)
ROOT = FILE.parents[0]
TEMPLATE = ROOT / 'templates'
app = Flask(__name__, template_folder=TEMPLATE)
app.secret_key = secrets.token_hex(16)  # 生成一个16字节的随机字符串作为密钥
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = './uploads/'  # 设置上传文件的存储目录
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 设置最大上传大小，例如16MB


if __name__ == '__main__':
    import Select_db
    from Algorithm_blueprint import alg_blueprint
    app.register_blueprint(Select_db.bp)
    alg_b = alg_blueprint(app)
    app.register_blueprint(alg_b.alg)
    app.run()
