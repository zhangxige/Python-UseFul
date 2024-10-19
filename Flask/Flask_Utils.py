# This is a demo for using libs (flask and sqlalchemy)
# Using flask and sqlalchemy create, select, query, update sqlite 
#  Next step, will focus on Web UI(html, css, javascript)
import pathlib

from flask import Flask, render_template, request, redirect


FILE = pathlib.Path(__file__)
ROOT = FILE.parents[0]
TEMPLATE = ROOT / 'templates'
app = Flask(__name__, template_folder=TEMPLATE)


@app.route("/login", methods=['GET', 'POST'])
def login_main():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    password = request.form.get('psd')
    # 判断用户名和密码
    if password and user:
        return redirect('/admin')
    else:
        error = '密码为空！'
        return render_template('login.html', error=error)


@app.route("/admin", methods=['GET', 'POST'])
def admin_main():
    return render_template('admin.html')


@app.route("/api", methods=['GET', 'POST'])
def api_test():
    return {'abc': 123, 'cd': "dvc"}


@app.route("/send", methods=['GET', 'POST'])
def send_test():
    info = request.json
    print(info)
    return 'ok, i recieve data!'


if __name__ == '__main__':
    import Select_db
    app.register_blueprint(Select_db.bp)
    app.run()
