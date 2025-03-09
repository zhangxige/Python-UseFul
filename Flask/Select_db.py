from flask import Blueprint
from flask import render_template, request

bp = Blueprint("db", __name__, url_prefix="/db")


@bp.route("/index", methods=("GET", "POST"))
def test_index():
    user = request.form.get('username')
    password = request.form.get('password')
    print(user)
    print(password)
    return render_template('test.html')


@bp.route("/select", methods=("GET", "POST"))
def select():
    info = {'a': 1, 'b': 2}
    return info
    # return render_template('test.html', posts=info)


# 数据库相关操作接口
class db_api:
    def __init__(self):
        pass

    # 查询
    # 添加
    # 删除
    # 修改
