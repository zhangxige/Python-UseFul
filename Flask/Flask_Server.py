# This is a demo for using libs (flask and sqlalchemy)
# Using flask and sqlalchemy create, select, query, update sqlite
#  Next step, will focus on Web UI(html, css, javascript)
import os
import pathlib
import secrets
from requests import request

from flask import Flask, redirect, render_template, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy


FILE = pathlib.Path(__file__)
ROOT = FILE.parents[0]
TEMPLATE = ROOT / 'templates'
app = Flask(__name__, template_folder=TEMPLATE)
app.secret_key = secrets.token_hex(16)  # 生成一个16字节的随机字符串作为密钥
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = './uploads/'  # 设置上传文件的存储目录
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 设置最大上传大小，例如16MB

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_db.db')
# 这里注意看，写的是URI，用来告诉程序你的数据库在什么地方存着
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
# SQLALCHEMY_COMMIT_TEARDOWN 因为数据库每次有变动的时候，数据改变，但不会自动的去改变数据库面的数据，
# 只有你去手动提交，告诉数据库要改变数据的时候才会改变，这里配置这个代表着，
# 不需要你手动的去提交了自动帮你提交了。也就是可以忽略 db.session.commit(
db = SQLAlchemy(app)


# 定义数据结构类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class sqlite3_api:
    s_api = Blueprint("sq", __name__, url_prefix="/sq")
    # 如果没有表要创建表，有的话则无改动
    with app.app_context():
        db.create_all()

    # 初始化db
    def __init__(self):
        pass

    # 查询数据
    @s_api.route("/sql")
    def find_all_users():
        users = User.query.all()
        print(users)
        return render_template("sql.html", users=users)

    # 查询一个数据
    @s_api.route("/get/<int:get_id>")
    def get_by_id(get_id):
        get_user = User.query.get(get_id)  # User.query.filter_by(id=get_id).first()
        return "编号：{0}，用戶名：{1}，邮箱：{2}".format(get_user.id, get_user.username, get_user.email)

    # 增加数据
    @s_api.route("/add/<username>")
    def add_user(username):
        new_user = User()
        new_user.username = username
        new_user.email = username + "@qq.com"
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    # 删除数据
    @s_api.route("/delete/<int:del_id>")
    def delete_by_id(del_id):
        del_user = User.query.filter_by(id=del_id).first()
        if del_user is not None:
            db.session.delete(del_user)
            db.session.commit()
        return redirect("/")

    @s_api.route("/update", methods=["GET", "POST"])
    def update():
        if request.method == "POST":
            user_id = request.form.get("id")
            new_username = request.form.get("username")
            new_email = request.form.get("email")
            user = User.query.get(user_id)
            if user:
                user.username = new_username
                user.email = new_email
                db.session.commit()
            return redirect(url_for("update"))
        users = User.query.all()
        return render_template("update.html", users=users)


if __name__ == '__main__':
    # from Select_blueprint import sqlite3_api
    from Algorithm_blueprint import alg_blueprint
    db_b = sqlite3_api()
    app.register_blueprint(db_b.s_api)
    alg_b = alg_blueprint(app)
    app.register_blueprint(alg_b.alg)
    app.run()
