import os
from flask import Blueprint, current_app
from flask import request, jsonify


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'ini'}  # 允许的文件类型


def allowed_file(filename):
    t = ('.' in filename) \
        and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return t


class alg_blueprint:
    alg = Blueprint("alg", __name__, url_prefix="/alg")

    def __init__(self, app):
        self.app = app
        pass

    # 返回无参数据
    @alg.route("/alg1", methods=("GET", "POST"))
    def select():
        info = {'a': 1, 'b': 2}
        # print("alg/alg1")s
        return info

    # post 提交json数据
    @alg.route("/alg2", methods=["POST"])
    def get_json():
        data = request.json  # 这是一个字典类型，可以直接访问键值对
        name = data.get('name', 'World')  # 获取'name'，如果没有则使用默认值'World'
        return jsonify({'message': f'Received name: {name}'})

    # post 提交图片或ini数据
    @alg.route("/alg3", methods=["GET", "POST"])
    def get_ini_img():
        # 检查是否有文件部分在请求中
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也会提交一个空的文件名，没有文件内容
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = file.filename.split(os.sep)[-1]
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                    filename)
            file.save(filepath)
            info = {'message': 'File uploaded successfully', 'path': filepath}
            return jsonify(info), 201
        else:
            return jsonify({'error': 'File type not allowed'}), 400
