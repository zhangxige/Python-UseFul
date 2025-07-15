from flask import Blueprint, render_template, request, redirect, url_for
from .model import User, db


class sqlite3_api:
    s_api = Blueprint("sq", __name__, url_prefix="/sq")
    # 如果没有表要创建表，有的话则无改动

    # 初始化db
    def __init__(self):
        pass

    # 查询数据
    @s_api.route("/queryall", methods=["GET", "POST"])
    def find_all_users():
        users = User.query.all()
        print(users)
        return render_template("sql.html", users=users)

    # 查询一个数据
    @s_api.route("/get/<int:get_id>")
    def get_by_id(get_id):
        # User.query.filter_by(id=get_id).first()
        get_user = User.query.get(get_id)
        info = [get_user.id, get_user.username, get_user.email]
        return "编号：{0}，用戶名：{1}，邮箱：{2}".format(*info)

    # 增加数据
    @s_api.route("/add/<username>", methods=["GET", "POST"])
    def add_user(username):
        new_user = User()
        new_user.username = username
        new_user.email = username + "@qq.com"
        db.session.add(new_user)
        db.session.commit()
        return redirect("/sq/queryall")

    # 删除数据
    @s_api.route("/delete/<int:del_id>")
    def delete_by_id(del_id):
        del_user = User.query.filter_by(id=del_id).first()
        if del_user is not None:
            db.session.delete(del_user)
            db.session.commit()
        return redirect("/sq/queryall")

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