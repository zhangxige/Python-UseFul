from flask import Flask
from .config import Config, setup_logging
from flask_cors import CORS  # 解决跨域问题


TEMPLATE = r'./templates'


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE)
    CORS(app)  # 解决跨域问题
    setup_logging()  # 设置日志配置
    app.config.from_object(Config)

    # 注册蓝图（如果使用）
    from .model import db
    from .model_view import sqlite3_api
    from .views.Algorithm_blueprint import alg_blueprint
    from .views.Select_blueprint import db_api
    from .views.Worker_blueprint import worker_blueprint
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # 添加 blueprint
    app.register_blueprint(sqlite3_api.s_api)
    app.register_blueprint(alg_blueprint.alg)
    app.register_blueprint(db_api.bp)
    app.register_blueprint(worker_blueprint.work)

    return app
